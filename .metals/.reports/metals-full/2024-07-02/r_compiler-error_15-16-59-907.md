file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### scala.MatchError: implicit class <error> extends  (of class scala.reflect.internal.Trees$ClassDef)

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
offset: 800
uri: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
text:
```scala
package com.sequoiareasoner.kernel.context

import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Props
import akka.actor.UntypedActor
import akka.pattern.ask

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
    implicit v@@
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
        while (counterActor ? 0 > 0) {} // now need to sort out this bit
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

    def onReceive(message: Any): Unit = message match {
        case 1 => counter.decrementAndGet()
        case -1 => counter.incrementAndGet()
        case 0 => {
            val theSender = sender()
            theSender ! counter.get()
        }
        case _ => throw new Exception(message.toString())
    }
}


```



#### Error stacktrace:

```
scala.tools.nsc.typechecker.Unapplies.constrParamss(Unapplies.scala:90)
	scala.tools.nsc.typechecker.Unapplies.factoryMeth(Unapplies.scala:141)
	scala.tools.nsc.typechecker.Unapplies.factoryMeth$(Unapplies.scala:138)
	scala.meta.internal.pc.MetalsGlobal$MetalsInteractiveAnalyzer.factoryMeth(MetalsGlobal.scala:76)
	scala.tools.nsc.typechecker.MethodSynthesis$MethodSynth.enterImplicitWrapper(MethodSynthesis.scala:238)
	scala.tools.nsc.typechecker.MethodSynthesis$MethodSynth.enterImplicitWrapper$(MethodSynthesis.scala:237)
	scala.tools.nsc.typechecker.Namers$Namer.enterImplicitWrapper(Namers.scala:58)
	scala.tools.nsc.interactive.InteractiveAnalyzer$InteractiveNamer.enterExistingSym(Global.scala:95)
	scala.tools.nsc.interactive.InteractiveAnalyzer$InteractiveNamer.enterExistingSym$(Global.scala:81)
	scala.tools.nsc.interactive.InteractiveAnalyzer$$anon$2.enterExistingSym(Global.scala:51)
	scala.tools.nsc.typechecker.Namers$Namer.standardEnterSym(Namers.scala:314)
	scala.tools.nsc.typechecker.AnalyzerPlugins.pluginsEnterSym(AnalyzerPlugins.scala:496)
	scala.tools.nsc.typechecker.AnalyzerPlugins.pluginsEnterSym$(AnalyzerPlugins.scala:495)
	scala.meta.internal.pc.MetalsGlobal$MetalsInteractiveAnalyzer.pluginsEnterSym(MetalsGlobal.scala:76)
	scala.tools.nsc.typechecker.Namers$Namer.enterSym(Namers.scala:288)
	scala.tools.nsc.typechecker.Typers$Typer.enterSym(Typers.scala:2010)
	scala.tools.nsc.typechecker.Typers$Typer.enterSyms(Typers.scala:2005)
	scala.tools.nsc.typechecker.Typers$Typer.typedTemplate(Typers.scala:2065)
	scala.tools.nsc.typechecker.Typers$Typer.typedClassDef(Typers.scala:1927)
	scala.tools.nsc.typechecker.Typers$Typer.typed1(Typers.scala:6060)
	scala.tools.nsc.typechecker.Typers$Typer.typed(Typers.scala:6153)
	scala.tools.nsc.typechecker.Typers$Typer.typedStat$1(Typers.scala:6231)
	scala.tools.nsc.typechecker.Typers$Typer.$anonfun$typedStats$8(Typers.scala:3470)
	scala.tools.nsc.typechecker.Typers$Typer.typedStats(Typers.scala:3470)
	scala.tools.nsc.typechecker.Typers$Typer.typedPackageDef$1(Typers.scala:5743)
	scala.tools.nsc.typechecker.Typers$Typer.typed1(Typers.scala:6063)
	scala.tools.nsc.typechecker.Typers$Typer.typed(Typers.scala:6153)
	scala.tools.nsc.typechecker.Analyzer$typerFactory$TyperPhase.apply(Analyzer.scala:124)
	scala.tools.nsc.Global$GlobalPhase.applyPhase(Global.scala:480)
	scala.tools.nsc.interactive.Global$TyperRun.applyPhase(Global.scala:1370)
	scala.tools.nsc.interactive.Global$TyperRun.typeCheck(Global.scala:1363)
	scala.tools.nsc.interactive.Global.typeCheck(Global.scala:680)
	scala.tools.nsc.interactive.Global.typedTreeAt(Global.scala:829)
	scala.tools.nsc.interactive.Global.completionsAt(Global.scala:1233)
	scala.meta.internal.pc.CompletionProvider.safeCompletionsAt(CompletionProvider.scala:506)
	scala.meta.internal.pc.CompletionProvider.completions(CompletionProvider.scala:58)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$complete$1(ScalaPresentationCompiler.scala:207)
```
#### Short summary: 

scala.MatchError: implicit class <error> extends  (of class scala.reflect.internal.Trees$ClassDef)