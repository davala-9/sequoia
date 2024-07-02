file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextStructureManager.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextStructureManager.scala:238: error: `identifier` expected but `]` found
  val saturationJobs: List[]
                           ^

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
uri: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextStructureManager.scala
text:
```scala
/*
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This file is part of Sequoia, an OWL 2 reasoner that supports the SRIQ subset of OWL 2 DL.
 * Copyright 2017 by Andrew Bate <code@andrewbate.com>.
 *
 * This code is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 only,
 * as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License version 3 for more details (a copy is
 * included in the LICENSE file that accompanied this code).
 *
 * You should have received a copy of the GNU General Public License
 * version 3 along with this work.  If not, see <http://www.gnu.org/licenses/>.
 */

package com.sequoiareasoner.kernel.context

import com.sequoiareasoner.kernel.clauses._
import com.sequoiareasoner.kernel.index.{ArrayBuilders, ImmutableSet, NeighborPredClauseIndex, TotalIRIMultiMap, _}
import com.sequoiareasoner.kernel.logging.Logger
import com.sequoiareasoner.kernel.owl.iri.IRI
import com.sequoiareasoner.kernel.owl.model.{NamedIndividual, OWLClass}
import com.sequoiareasoner.kernel.structural.DLOntology
import com.sequoiareasoner.kernel.taxonomy.Taxonomy
import org.semanticweb.owlapi.model.OWLNamedIndividual

import scala.collection.mutable
import scala.collection.JavaConverters._
import scala.concurrent.Await
import scala.concurrent.Future

import java.util.concurrent.ForkJoinPool
import java.util.concurrent.Callable

/** Class that manages the context structure, including the introducing of new contexts according to a supplied strategy
  * function, and the termination of the procedure once all contexts have completed saturation. */

 /** IMPORTANT INFORMATION: Currently, the Context Structure Manager is hardcoded to, on creation, run only once,
   * and check all atomic queries of the form A(x) -> B(x), for A(x) an OWLClass in the input ontology
   * this includes auxiliary classes for nominals.
   * In the future, we will implement a more fine degree of control of which queries have been checked,
   * to allow for shorter computations and incremental reasoning. */

final class ContextStructureManager(ontology: DLOntology,
                                    redundancyIndex: => ContextClauseRedundancyIndex,
                                    enableEqualityReasoning: Boolean,
                                    equalityOptimization: => EqualityOptimization,
                                    strategy: ImmutableSet[Predicate] => ImmutableSet[Predicate],
                                    targetConcepts: Set[Int],
                                    logger: Logger) {

  if (ontology eq null) throw new NullPointerException

 //  require(query.keys.forall( x => IRI(x).isImported || IRI(x).isInternalIndividual || IRI(x).isThing))
//  require(query.values.flatten.forall( x => IRI(x).isImported || IRI(x).isInternalIndividual || IRI(x).isThing))


  /**------------------------- Context Structure fields and methods------------------------ */


  /** This map provides, for each set of predicates, a channel to the context that has that set as its core */
  private[this] val contexts = new mutable.AnyRefMap[ImmutableSet[Predicate], ContextRunnable]
  // private[this] val contextExecutor = new ForkJoinPool() // Defaults to number of processors -1
  private[this] val contextExecutor = new ActorExecutionService()
  def messageContext(context: ContextRunnable, message: InterContextMessage): Unit = {
    val task: Runnable = () => { context.reSaturateUponMessage(message) }
    contextExecutor.executeWithPartition(task, context)
  }

  /** This map provides, for each nominal context O(x), the set of (other) contexts that mention o */
  private[this] val constantIndex = new mutable.AnyRefMap[Constant,collection.mutable.Set[ImmutableSet[Predicate]]]
  /** Add a context to the index mapping each constant to the list of contexts that mention it */
  def addToConstantIndex(individual: Constant, core: ImmutableSet[Predicate]) = synchronized {
    constantIndex.getOrElseUpdate(individual, collection.mutable.Set[ImmutableSet[Predicate]]()) += core
    Unit
  }

  /** `superConcepts(a)` collects subsumption relations between  all the (direct and non-direct) super concepts of `a`. */
  private[this] val provedAtomicQueries = new TotalIRIMultiMap[IRI](ArrayBuilders.iriArrayBuilder)

  /** This records whether a contradiction clause has been derived.  */
  //TODO: stop reasoner whenever inconsistency has been derived
  var contradictionDerived = false
  def flagOntologyAsInconsistent(): Unit = synchronized { contradictionDerived = true }
  def contradictionHasBeenDerived: Boolean = synchronized { contradictionDerived }


   /**-------------------------- Flow Control --------------------------*/


  private[this] var beginTime: Long = 0L
  private[this] var totalTime: Long = 0L
  private[this] var hornPhaseActive: Boolean = true
  
  /** Stop ASAP the construction of the context structure */
  def interrupt(): Unit = synchronized {
    if (ontology.havocTriggered) contextExecutor.shutdownNow()
  }



   // Uncommenting for the Kaminsky optimisation
   private[this] val certainFacts: mutable.Map[Int,mutable.Set[Int]] = ontology.ensureTrivialFactsAddedAndGetABox
   def addCertainGroundFact(predicate: Int, nominal: Int) = synchronized {
     certainFacts.getOrElseUpdate(nominal, collection.mutable.Set[Int]()) += predicate
   }
//   private[this] val derivedNewCertainGroundFacts = collection.immutable.HashSet[Predicate]()
   def getCertainFacts(nominal: Int) = synchronized {
     certainFacts(nominal)
   }
//   def getCertainGroundFacts(ordering: ContextLiteralOrdering): Seq[ContextClause] = synchronized {
//     (for ( (k,v) <- certainFacts.iterator; pred <- v) yield ContextClause(Array[Predicate](),
//       Array[Literal](Concept(IRI(pred),Term(IRI.importedIriUid2IriNameString(k)))(ontology)))(ordering)).toSeq
//   }

  /** -------------------------- Operations on the context structure -------------------*/


  private[this] def buildContext(queryConcepts: Set[Int],
                                 core: ImmutableSet[Predicate],
                                 rootContext: Boolean,
                                 workedOffClauseIndex: ContextClauseIndex,
                                 ordering: ContextLiteralOrdering,
                                 hornPhaseActive: Boolean): Callable[ContextRunnable] = () => {
   // Ignore this parameter for the moment. Require(ordering.verifyQuery(queryConcepts))
    val state = if (core.toSeq.head.iri.isInternalIndividual) {
      new NominalContextState(queryConcepts, core, rootContext, workedOffClauseIndex,
        new NeighborPredClauseIndex, equalityOptimization, redundancyIndex, hornPhaseActive,ordering,ontology, contextStructureManager = this)
    } else {
      new ContextState(queryConcepts, core, rootContext, workedOffClauseIndex, new NeighborPredClauseIndex,
        equalityOptimization, redundancyIndex, hornPhaseActive, ordering, ontology, contextStructureManager = this)
    }
    new ContextRunnable(state, ontology, enableEqualityReasoning, ordering, contextStructureManager = this)
  }

  def getAllContexts: Iterable[ContextRunnable] = synchronized { contexts.values }

  /** Given a conjunction of known predicates, this method identifies the successor given by the _strategy_ of this
    * context structure, and then retrieves it or creates it; in the latter case, it initialises the first round */
  def getSuccessor(K1: ImmutableSet[Predicate]): ContextRunnable = synchronized {
    val core: ImmutableSet[Predicate] = strategy(K1)
    if (core.isEmpty) logger.warn(s"WARNING: trivial context is active! (K1 = $K1)")
    contexts.getOrElseUpdate(core, {
      /** If we create the context, then it is not a root context so the Index is a standard ContextClauseIndex */
      val contextIndex = new ContextClauseIndex
      /** Since this is not a root context, the query is empty */
      val ordering = ContextLiteralOrdering(Set[Int]())
      val createNewContext: Callable[ContextRunnable] = buildContext(Set[Int](), core, rootContext = false, contextIndex, ordering, hornPhaseActive)
      val context: ContextRunnable = contextExecutor.submit(createNewContext).get
      contextExecutor.executeWithPartition(context.saturateAndPush(), context)
      context
    })
  }
  /** Given a constant, retrieve or create the nominal context corresponding to that constant. If it is created,
    * the initialisation round is started.*/
  protected[context] def getNominalContext(individual: Constant) : ContextRunnable = synchronized {
    implicit val theOntology = ontology
    val core: ImmutableSet[Predicate] = ImmutableSet(Concept(IRI.nominalConcept(individual.toString),CentralVariable))
    contexts.getOrElseUpdate(core, {
      // System.out.println("NOMINAL NODE CREATED for core " + core + " !!")
      /** Since each nominal context is a root context, we introduce a root context index */
      val contextIndex = new RootContextClauseIndex(provedAtomicQueries.addKey(IRI.nominalConcept(individual.toString)))
      /** Since nominal contexts have no query, the query is empty */
      val ordering = ContextLiteralOrdering(Set[Int]())
      val createNewContext: Callable[ContextRunnable] = buildContext(Set[Int](), core, rootContext = true, contextIndex, ordering, hornPhaseActive)
      val context: ContextRunnable = contextExecutor.submit(createNewContext).get
      contextExecutor.executeWithPartition(context.saturateAndPush(), context)
      context
    })
  }
  protected[context] def getContextsWithNominal(individual: Constant): Iterable[ImmutableSet[Predicate]] = synchronized {
    constantIndex(individual)
  }


  /** ------------------------------ Output Methods -------------------------------------- */

  def getClassesTaxonomy: Taxonomy[OWLClass] = {
    val classHierarchy = new TotalIRIMultiMap[IRI](ArrayBuilders.iriArrayBuilder)
    provedAtomicQueries.foreachKeys(key => {
//      println("provedAtomicQuery key: ")
//      println(key)
//      println("Values")
//      provedAtomicQueries(key).foreach( iri => println(iri))
//      println("Is empty?: " + provedAtomicQueries(key).isEmpty)
      if (key.isImported) provedAtomicQueries(key).foreach(value => classHierarchy.addBinding(key, value))
    })
    Taxonomy[OWLClass](classHierarchy, Some(IRI.owlNothing), Some(IRI.owlThing))
  }

  def getIndividualsTaxonomy: Taxonomy[NamedIndividual] = {
    val individualHierarchy = new TotalIRIMultiMap[IRI](ArrayBuilders.iriArrayBuilder)
    provedAtomicQueries.foreachKeys(key => {
      if (key.isInternalIndividual) provedAtomicQueries(key).foreach(value =>
        individualHierarchy.addBinding(IRI(IRI.nominalConceptUid2NominalIriStringName(key.uid)), value))
    })
    Taxonomy[NamedIndividual](individualHierarchy)
  }

  /** -------------------- Saturation of the Context Structure (ON CREATION) ------------------- */

  def waitForFinish() = {
    var count: Int = 1
    while (count != 0) {
      count = contexts.values.filter(c => c.active).size
      if (count == 0) {
        // contexts.values.foreach(c => println(c.active))
      } else println("Active contexts: " + count)
      Thread.sleep(1000)
    }
  }


  beginTime = System.currentTimeMillis
  
  /** Create jobs to create a context for each target concept, then run those jobs */
  implicit val theOntology = ontology

  val contextCreationJobs: Set[Callable[ContextRunnable]] = targetConcepts.map(concept => {
    val core: ImmutableSet[Predicate] = ImmutableSet(Concept(IRI(concept),CentralVariable))
    /** Creates the context index, which is a special case since these contexts are query contexts. */
    val contextIndex = new RootContextClauseIndex(provedAtomicQueries.addKey(IRI(concept)))
    buildContext(queryConcepts = Set.empty[Int], core, rootContext = true, contextIndex,
      ContextLiteralOrdering(), hornPhaseActive)
  })
  val cs = contextExecutor.invokeAll(contextCreationJobs.asJava).asScala.map(x => x.get())
  for (c <- cs) contexts.put(c.state.core, c)
  println("creation jobs done")

  /** Saturate every concept, starting with the Horn phase */
  // val saturationJobs: List[(ContextRunnable, Runnable)] = cs.toList.map(c => (c, c.saturateAndPush()))
  // saturationJobs.foreach(x => contextExecutor.executeWithPartition(x._2, x._1))
  val saturationJobs: List[]
  waitForFinish()
  
  println("saturation jobs done")

  /** Non-Horn phase */
  hornPhaseActive = false
  val nonHornJobs: List[(ContextRunnable, Runnable)] = getAllContexts.toList.map(c => (
      c,
      (() => c.reSaturateUponMessage(StartNonHornPhase())): Runnable
    )
  )
  nonHornJobs.foreach(x => contextExecutor.executeWithPartition(x._2, x._1))
  
  waitForFinish()
  println("non horn jobs done")
  println("Number of contexts created: " + contexts.size)

}




```



#### Error stacktrace:

```
scala.meta.internal.parsers.Reporter.syntaxError(Reporter.scala:16)
	scala.meta.internal.parsers.Reporter.syntaxError$(Reporter.scala:16)
	scala.meta.internal.parsers.Reporter$$anon$1.syntaxError(Reporter.scala:22)
	scala.meta.internal.parsers.Reporter.syntaxError(Reporter.scala:17)
	scala.meta.internal.parsers.Reporter.syntaxError$(Reporter.scala:17)
	scala.meta.internal.parsers.Reporter$$anon$1.syntaxError(Reporter.scala:22)
	scala.meta.internal.parsers.ScalametaParser.syntaxErrorExpected(ScalametaParser.scala:387)
	scala.meta.internal.parsers.ScalametaParser.name(ScalametaParser.scala:1131)
	scala.meta.internal.parsers.ScalametaParser.termName(ScalametaParser.scala:1134)
	scala.meta.internal.parsers.ScalametaParser.path(ScalametaParser.scala:1181)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.pathSimpleType$1(ScalametaParser.scala:965)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType(ScalametaParser.scala:1013)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType$(ScalametaParser.scala:956)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.simpleType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.annotType(ScalametaParser.scala:949)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$compoundType$1(ScalametaParser.scala:924)
	scala.Option.getOrElse(Option.scala:201)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.compoundType(ScalametaParser.scala:922)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.compoundType$(ScalametaParser.scala:922)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.compoundType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixType(ScalametaParser.scala:855)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixType$(ScalametaParser.scala:854)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.infixType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixTypeOrTuple(ScalametaParser.scala:851)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixTypeOrTuple$(ScalametaParser.scala:849)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.infixTypeOrTuple(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$typ$1(ScalametaParser.scala:782)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typ(ScalametaParser.scala:778)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typ$(ScalametaParser.scala:778)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.typ(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$types$1(ScalametaParser.scala:1028)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$commaSeparated$1(ScalametaParser.scala:632)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$commaSeparated$1$adapted(ScalametaParser.scala:632)
	scala.meta.internal.parsers.ScalametaParser.iter$1(ScalametaParser.scala:622)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$tokenSeparated$1(ScalametaParser.scala:627)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$tokenSeparated$1$adapted(ScalametaParser.scala:615)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:555)
	scala.meta.internal.parsers.ScalametaParser.tokenSeparated(ScalametaParser.scala:615)
	scala.meta.internal.parsers.ScalametaParser.commaSeparatedWithIndex(ScalametaParser.scala:636)
	scala.meta.internal.parsers.ScalametaParser.commaSeparated(ScalametaParser.scala:632)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.types(ScalametaParser.scala:1028)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.types$(ScalametaParser.scala:1028)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.types(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$typeArgs$3(ScalametaParser.scala:847)
	scala.meta.internal.parsers.ScalametaParser.inBrackets(ScalametaParser.scala:291)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$typeArgs$2(ScalametaParser.scala:847)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$typeArgs$1(ScalametaParser.scala:847)
	scala.meta.internal.parsers.NestedContext.within(NestedContext.scala:8)
	scala.meta.internal.parsers.NestedContext.within$(NestedContext.scala:6)
	scala.meta.internal.parsers.ScalametaParser$TypeBracketsContext$.within(ScalametaParser.scala:42)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typeArgs(ScalametaParser.scala:847)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typeArgs$(ScalametaParser.scala:846)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.typeArgs(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$simpleTypeRest$2(ScalametaParser.scala:1024)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleTypeRest(ScalametaParser.scala:1024)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType(ScalametaParser.scala:1015)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType$(ScalametaParser.scala:956)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.simpleType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.annotType(ScalametaParser.scala:949)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$compoundType$1(ScalametaParser.scala:924)
	scala.Option.getOrElse(Option.scala:201)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.compoundType(ScalametaParser.scala:922)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.compoundType$(ScalametaParser.scala:922)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.compoundType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixType(ScalametaParser.scala:855)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixType$(ScalametaParser.scala:854)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.infixType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixTypeOrTuple(ScalametaParser.scala:851)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.infixTypeOrTuple$(ScalametaParser.scala:849)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.infixTypeOrTuple(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.$anonfun$typ$1(ScalametaParser.scala:782)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typ(ScalametaParser.scala:778)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.typ$(ScalametaParser.scala:778)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.typ(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser.typ(ScalametaParser.scala:2714)
	scala.meta.internal.parsers.ScalametaParser.typedOpt(ScalametaParser.scala:1357)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$patDefOrDcl$1(ScalametaParser.scala:3339)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:371)
	scala.meta.internal.parsers.ScalametaParser.patDefOrDcl(ScalametaParser.scala:3330)
	scala.meta.internal.parsers.ScalametaParser.defOrDclOrSecondaryCtor(ScalametaParser.scala:3299)
	scala.meta.internal.parsers.ScalametaParser.nonLocalDefOrDcl(ScalametaParser.scala:3283)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$templateStat$1.applyOrElse(ScalametaParser.scala:4137)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$templateStat$1.applyOrElse(ScalametaParser.scala:4134)
	scala.PartialFunction.$anonfun$runWith$1(PartialFunction.scala:231)
	scala.PartialFunction.$anonfun$runWith$1$adapted(PartialFunction.scala:230)
	scala.meta.internal.parsers.ScalametaParser.statSeqBuf(ScalametaParser.scala:4094)
	scala.meta.internal.parsers.ScalametaParser.getStats$2(ScalametaParser.scala:4124)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$scala$meta$internal$parsers$ScalametaParser$$templateStatSeq$3(ScalametaParser.scala:4125)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$scala$meta$internal$parsers$ScalametaParser$$templateStatSeq$3$adapted(ScalametaParser.scala:4123)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:555)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$templateStatSeq(ScalametaParser.scala:4123)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$templateStatSeq(ScalametaParser.scala:4115)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$templateBody$1(ScalametaParser.scala:3993)
	scala.meta.internal.parsers.ScalametaParser.inBracesOr(ScalametaParser.scala:254)
	scala.meta.internal.parsers.ScalametaParser.inBraces(ScalametaParser.scala:250)
	scala.meta.internal.parsers.ScalametaParser.templateBody(ScalametaParser.scala:3993)
	scala.meta.internal.parsers.ScalametaParser.templateBodyOpt(ScalametaParser.scala:3996)
	scala.meta.internal.parsers.ScalametaParser.templateAfterExtends(ScalametaParser.scala:3947)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$templateOpt$1(ScalametaParser.scala:3988)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.templateOpt(ScalametaParser.scala:3980)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$classDef$1(ScalametaParser.scala:3641)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:371)
	scala.meta.internal.parsers.ScalametaParser.classDef(ScalametaParser.scala:3619)
	scala.meta.internal.parsers.ScalametaParser.tmplDef(ScalametaParser.scala:3583)
	scala.meta.internal.parsers.ScalametaParser.topLevelTmplDef(ScalametaParser.scala:3573)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$2.applyOrElse(ScalametaParser.scala:4108)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$2.applyOrElse(ScalametaParser.scala:4102)
	scala.PartialFunction.$anonfun$runWith$1(PartialFunction.scala:231)
	scala.PartialFunction.$anonfun$runWith$1$adapted(PartialFunction.scala:230)
	scala.meta.internal.parsers.ScalametaParser.statSeqBuf(ScalametaParser.scala:4094)
	scala.meta.internal.parsers.ScalametaParser.bracelessPackageStats$1(ScalametaParser.scala:4288)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$batchSource$11(ScalametaParser.scala:4300)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$batchSource$10(ScalametaParser.scala:4300)
	scala.meta.internal.parsers.ScalametaParser.tryParse(ScalametaParser.scala:206)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$batchSource$1(ScalametaParser.scala:4292)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.batchSource(ScalametaParser.scala:4261)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$source$1(ScalametaParser.scala:4255)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.source(ScalametaParser.scala:4255)
	scala.meta.internal.parsers.ScalametaParser.entrypointSource(ScalametaParser.scala:4259)
	scala.meta.internal.parsers.ScalametaParser.parseSourceImpl(ScalametaParser.scala:119)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$parseSource$1(ScalametaParser.scala:116)
	scala.meta.internal.parsers.ScalametaParser.parseRuleAfterBOF(ScalametaParser.scala:58)
	scala.meta.internal.parsers.ScalametaParser.parseRule(ScalametaParser.scala:53)
	scala.meta.internal.parsers.ScalametaParser.parseSource(ScalametaParser.scala:116)
	scala.meta.parsers.Parse$.$anonfun$parseSource$1(Parse.scala:30)
	scala.meta.parsers.Parse$$anon$1.apply(Parse.scala:37)
	scala.meta.parsers.Api$XtensionParseDialectInput.parse(Api.scala:22)
	scala.meta.internal.semanticdb.scalac.ParseOps$XtensionCompilationUnitSource.toSource(ParseOps.scala:15)
	scala.meta.internal.semanticdb.scalac.TextDocumentOps$XtensionCompilationUnitDocument.toTextDocument(TextDocumentOps.scala:179)
	scala.meta.internal.pc.SemanticdbTextDocumentProvider.textDocument(SemanticdbTextDocumentProvider.scala:54)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$semanticdbTextDocument$1(ScalaPresentationCompiler.scala:462)
```
#### Short summary: 

file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextStructureManager.scala:238: error: `identifier` expected but `]` found
  val saturationJobs: List[]
                           ^