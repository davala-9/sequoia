file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:33: error: `identifier` expected but `=` found
    def executeWithPartition(command: Callable[Any], c: ContextRunnable):  = {
                                                                           ^

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
uri: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
text:
```scala
package com.sequoiareasoner.kernel.context

import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Props
import akka.actor.UntypedActor
import akka.actor.Actor
import akka.pattern.ask
import akka.util.Timeout

import java.util.Collections
import java.util.List
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit
import java.util.function.Function
import java.util.concurrent.ForkJoinPool
import java.util.concurrent.atomic.AtomicInteger

import scala.concurrent.Await
import scala.concurrent.Future
import scala.concurrent.duration.Duration
import scala.concurrent.duration.MINUTES
import scala.util.Try
import java.util.concurrent.ForkJoinTask


class ActorExecutionService extends ForkJoinPool {
    val actorSystem: ActorSystem = ActorSystem.create("context-actor-system")
    val actors: ConcurrentHashMap[String,ActorRef] = new ConcurrentHashMap()

    def executeWithPartition(command: Callable[Any], c: ContextRunnable):  = {
        c.active = true
        val partitionKey = c.state.core.toString.replaceAll("[^a-zA-Z]", "")
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        actorRef.tell(command, actorRef)
    }

    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props(new ExecutionServiceActor), partitionKey)
    }

}

class ExecutionServiceActor extends Actor {
    def receive: Receive = {
        case runnable: Runnable => runnable.run()
        case m => throw new Exception(m.toString())
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
	scala.meta.internal.parsers.ScalametaParser.typ(ScalametaParser.scala:2714)
	scala.meta.internal.parsers.ScalametaParser.typedOpt(ScalametaParser.scala:1357)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$funDefRest$2(ScalametaParser.scala:3518)
	scala.meta.internal.parsers.NestedContext.within(NestedContext.scala:8)
	scala.meta.internal.parsers.NestedContext.within$(NestedContext.scala:6)
	scala.meta.internal.parsers.ScalametaParser$ReturnTypeContext$.within(ScalametaParser.scala:41)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$funDefRest$1(ScalametaParser.scala:3518)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:371)
	scala.meta.internal.parsers.ScalametaParser.funDefRest(ScalametaParser.scala:3495)
	scala.meta.internal.parsers.ScalametaParser.funDefOrDclOrExtensionOrSecondaryCtor(ScalametaParser.scala:3444)
	scala.meta.internal.parsers.ScalametaParser.defOrDclOrSecondaryCtor(ScalametaParser.scala:3304)
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
	scala.meta.internal.parsers.ScalametaParser.$anonfun$template$1(ScalametaParser.scala:3963)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.template(ScalametaParser.scala:3952)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$templateOpt$1(ScalametaParser.scala:3987)
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

file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:33: error: `identifier` expected but `=` found
    def executeWithPartition(command: Callable[Any], c: ContextRunnable):  = {
                                                                           ^