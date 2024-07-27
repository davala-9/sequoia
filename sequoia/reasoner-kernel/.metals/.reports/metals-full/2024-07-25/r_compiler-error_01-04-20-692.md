file://<WORKSPACE>/src/main/scala/com/sequoiareasoner/kernel/context/ContextAwareForkJoinPool.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextAwareForkJoinPool.scala:19: error: `type` expected but `(` found
    val pool: Executor = new Executors.()
                                       ^

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
uri: file://<WORKSPACE>/src/main/scala/com/sequoiareasoner/kernel/context/ContextAwareForkJoinPool.scala
text:
```scala
package com.sequoiareasoner.kernel.context

import com.sequoiareasoner.kernel.clauses._
import com.sequoiareasoner.kernel.index._
import com.sequoiareasoner.kernel.structural.DLOntology
import com.sequoiareasoner.arrayops._
import com.sequoiareasoner.kernel.logging.DerivationObserver
import com.sequoiareasoner.kernel.owl.iri.IRI

import java.util.concurrent.Callable
import java.util.concurrent.ForkJoinPool
import java.util.concurrent.ForkJoinTask
import java.util.concurrent.atomic.AtomicBoolean
import java.util.Set
import java.util.concurrent.Future
import java.util.concurrent.Executors

class ContextAwareForkJoinPool {
    val pool: Executor = new Executors.()

    def submit(task: Callable[ContextRunnable]): Future[ContextRunnable] = {
        pool.submit(task)
    }

    def submitUnit(task: Callable[Unit]): Future[Unit] = {
        pool.submit(task)
    }

    def invokeAll(tasks: Set[Callable[ContextRunnable]]): java.util.List[Future[ContextRunnable]] = {
        pool.invokeAll(tasks)
    }

    def pullFromQueue(context: ContextRunnable): Future[Unit] = context.queue.synchronized {
        if (!context.queue.isEmpty) {
            execute(context.queue.poll(), context)
        } else return null
    }

    def execute(task: Callable[Unit], context: ContextRunnable): Future[Unit] = {
        if (context.active.compareAndSet(false, true)) { // if context is not active, set it to active and submit the task to pool
            val c: Callable[Unit] = () => { task.call(); context.setInactive() }
            pool.submit(c)
        } else { // if context is already active, queue the task to the context
            context.queue.put(task)
            if (context.active.compareAndSet(false, true)) { // if context is not active, set it to active and submit the task to pool
                pullFromQueue(context)
            } else return null
        }
    }

    def isQuiescent(): Boolean = {
        pool.isQuiescent()
    }

    def getActiveThreadCount(): Int = {
        pool.getActiveThreadCount()
    }

    def shutdownNow(): Unit = {
        pool.shutdownNow()
    }

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
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$expectAt(ScalametaParser.scala:389)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$expectAt(ScalametaParser.scala:393)
	scala.meta.internal.parsers.ScalametaParser.expect(ScalametaParser.scala:395)
	scala.meta.internal.parsers.ScalametaParser.accept(ScalametaParser.scala:411)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.pathSimpleType$1(ScalametaParser.scala:980)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType(ScalametaParser.scala:985)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.simpleType$(ScalametaParser.scala:956)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.simpleType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.annotType(ScalametaParser.scala:949)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.annotType(ScalametaParser.scala:946)
	scala.meta.internal.parsers.ScalametaParser$PatternContextSensitive.annotType$(ScalametaParser.scala:945)
	scala.meta.internal.parsers.ScalametaParser$outPattern$.annotType(ScalametaParser.scala:2698)
	scala.meta.internal.parsers.ScalametaParser.startModType(ScalametaParser.scala:2720)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$initInsideTemplate$1(ScalametaParser.scala:3783)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$initRest$1(ScalametaParser.scala:3807)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.initRest(ScalametaParser.scala:3798)
	scala.meta.internal.parsers.ScalametaParser.initInsideTemplate(ScalametaParser.scala:3783)
	scala.meta.internal.parsers.ScalametaParser.init(ScalametaParser.scala:3915)
	scala.meta.internal.parsers.ScalametaParser.templateParents(ScalametaParser.scala:3922)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$template$1(ScalametaParser.scala:3962)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.template(ScalametaParser.scala:3952)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$simpleExpr0$2(ScalametaParser.scala:2064)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2062)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2041)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2038)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:1904)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1533)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1457)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1374)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$patDefOrDcl$1(ScalametaParser.scala:3342)
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

file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextAwareForkJoinPool.scala:19: error: `type` expected but `(` found
    val pool: Executor = new Executors.()
                                       ^