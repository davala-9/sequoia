file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:63: error: `;` expected but `]` found
        }]
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


import java.util.Collections
import java.util.List
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit
import java.util.function.Function
import java.util.concurrent.ForkJoinPool
import java.util.concurrent.atomic.AtomicInteger


class ActorExecutionService extends ForkJoinPool {
    val actorSystem: ActorSystem = ActorSystem.create("context-actor-system")
    val actors: ConcurrentHashMap[String,ActorRef] = new ConcurrentHashMap()
    // val counter = new AtomicInteger(0)
    val counterActor: ActorRef = actorSystem.actorOf(Props.create(classOf[CounterActor]), "counter")

    def executeWithPartition(command: Runnable, partitionKey: String): Unit = {
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        // counterActor.tell(1, actorRef)
        actorRef.tell(
            (() => command.run()): Runnable, 
            actorRef)
    }

    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props.create(classOf[ExecutionServiceActor]), partitionKey)
    }

    def waitForFinish() = {
        while (counterActor.getCount > 0) {} // now need to sort out this bit
    }
    
    class ExecutionServiceActor extends UntypedActor {
        def onReceive(message: Any): Unit = message match {
            case runnable: Runnable => {
                counterActor ! 1
                runnable.run()
                counterActor ! -1
            }
            case _ => throw new Exception(message.toString())
       }
    }
}

class CounterActor extends UntypedActor {
    val counter = new AtomicInteger(0)
    def getCount = counter.get()

    def onReceive(message: Any): Unit = message match {
        case 1 => counter.decrementAndGet()
        case -1 => counter.incrementAndGet()
        case 0 => {
            val sender = sender()
        }]
        case _ => throw new Exception(message.toString())
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
	scala.meta.internal.parsers.ScalametaParser.acceptStatSep(ScalametaParser.scala:443)
	scala.meta.internal.parsers.ScalametaParser.iter$7(ScalametaParser.scala:4223)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1(ScalametaParser.scala:4234)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1$adapted(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:555)
	scala.meta.internal.parsers.ScalametaParser.blockStatSeq(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.parseStatSeq$1(ScalametaParser.scala:2384)
	scala.meta.internal.parsers.ScalametaParser.caseBody$1(ScalametaParser.scala:2391)
	scala.meta.internal.parsers.ScalametaParser.caseClause(ScalametaParser.scala:2395)
	scala.meta.internal.parsers.ScalametaParser.iter$5(ScalametaParser.scala:2423)
	scala.meta.internal.parsers.ScalametaParser.caseClausesIfAny(ScalametaParser.scala:2429)
	scala.meta.internal.parsers.ScalametaParser.caseClauses(ScalametaParser.scala:2406)
	scala.meta.internal.parsers.ScalametaParser.matchClause(ScalametaParser.scala:1409)
	scala.meta.internal.parsers.ScalametaParser.iter$3(ScalametaParser.scala:1573)
	scala.meta.internal.parsers.ScalametaParser.exprOtherRest(ScalametaParser.scala:1577)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1534)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1457)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1374)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$funDefRest$1(ScalametaParser.scala:3531)
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

file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:63: error: `;` expected but `]` found
        }]
         ^