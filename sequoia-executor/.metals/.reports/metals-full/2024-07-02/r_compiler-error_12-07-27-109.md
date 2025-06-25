file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### scala.reflect.internal.FatalError: 
  unexpected tree: class scala.reflect.internal.Trees$Template
scala.AnyRef
     while compiling: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
        during phase: globalPhase=<no phase>, enteringPhase=parser
     library version: version 2.13.12
    compiler version: version 2.13.12
  reconstructed args: -classpath <HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar -Ymacro-expand:discard -Ycache-plugin-class-loader:last-modified -Ypresentation-any-thread

  last tree to typer: Template
       tree position: line 66 of file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
              symbol: <none>
   symbol definition: <none> (a NoSymbol)
      symbol package: <none>
       symbol owners: 
           call site: <none> in <none>

== Source file context for tree position ==

    63 
    64     def waitForFinish() = {
    65 
    66         actors.forEachValue(1, actor: ActorRef => {
    67             actor.t
    68         })
    69         while (active.get() > 0) {

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
offset: 2381
uri: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
text:
```scala
package com.sequoiareasoner.kernel.context

import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Props
import akka.actor.UntypedActor
import akka.pattern.gracefulStop

import scala.concurrent.duration.FiniteDuration

import java.util.Collections
import java.util.List
import java.util.concurrent.AbstractExecutorService
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.ExecutorService
import java.util.concurrent.TimeUnit
import java.util.function.Function
import java.util.concurrent.ForkJoinPool
import java.util.concurrent.atomic.AtomicInteger


// class ActorDemo {

//     public static void main( String[] args ) throws InterruptedException {
//         // The following partitioner will spread the requests over
//         // multiple actors, which I chose to demonstrate the technique.
//         // You will need to change it to one that better maps the the
//         // jobs to your use case.   Remember that jobs that get mapped
//         // to the same key, will get executed in serial (probably
//         // but not necessarily) by the same thread.
//         ExecutorService exectorService = new ActorExecutionService( job -> job.hashCode()+"" );

//         for ( int i=0; i<100; i++ ) {
//             int id = i;
//             exectorService.submit( () -> System.out.println("JOB " + id) );
//         }

//         exectorService.shutdown();
//         exectorService.awaitTermination( 1, TimeUnit.MINUTES );

//         System.out.println( "DONE" );
//     }

// }


class ActorExecutionService extends ForkJoinPool {
    val actorSystem: ActorSystem = ActorSystem.create("context-actor-system")
    val actors: ConcurrentHashMap[String,ActorRef] = new ConcurrentHashMap()
    val active: AtomicInteger = new AtomicInteger(0)

    def executeWithPartition(command: Runnable, partitionKey: String): Unit = {
        active.incrementAndGet()
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        actorRef.tell(
            () => { command.run(); active.decrementAndGet() }, 
            actorRef)
    }

    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props.create(classOf[ExecutionServiceActor]), partitionKey)
    }

    def waitForFinish() = {

        actors.forEachValue(1, actor: ActorRef => {
            acto@@r.t
        })
        while (active.get() > 0) {
            println(active.get())
            Thread.sleep(100)
        }
    }


    // def shutdown(): Unit = {
    //     actorSystem.terminate()
    // }

    // def shutdownNow(): List[Runnable] = {
    //     actorSystem.terminate()

    //     try {
    //         awaitTermination( 1, TimeUnit.MINUTES )
    //     } catch {
    //         case e: InterruptedException => throw new RuntimeException(e)
    //     }

    //     return Collections.emptyList()
    // }

    // def isShutdown(): Boolean = {
    //     return actorSystem.isTerminated()
    // }

    // def isTerminated(): Boolean = {
    //     return actorSystem.isTerminated()
    // }

    // def awaitTermination(timeout: Long, unit: TimeUnit): Boolean = {
    //     actorSystem.awaitTermination()

    //     return actorSystem.isTerminated()
    // }
}

class ExecutionServiceActor extends UntypedActor {
   def onReceive(message: Any): Unit = message match {
       case runnable: Runnable => runnable.run()
       case _ => throw new Exception(message.toString())
   }
}
```



#### Error stacktrace:

```
scala.reflect.internal.Reporting.abort(Reporting.scala:70)
	scala.reflect.internal.Reporting.abort$(Reporting.scala:66)
	scala.reflect.internal.SymbolTable.abort(SymbolTable.scala:28)
	scala.tools.nsc.typechecker.Typers$Typer.typedOutsidePatternMode$1(Typers.scala:6090)
	scala.tools.nsc.typechecker.Typers$Typer.typed1(Typers.scala:6107)
	scala.tools.nsc.typechecker.Typers$Typer.typed(Typers.scala:6153)
	scala.tools.nsc.typechecker.Typers$Typer.typedQualifier(Typers.scala:6251)
	scala.meta.internal.pc.PcDefinitionProvider.definitionTypedTreeAt(PcDefinitionProvider.scala:160)
	scala.meta.internal.pc.PcDefinitionProvider.definition(PcDefinitionProvider.scala:68)
	scala.meta.internal.pc.PcDefinitionProvider.definition(PcDefinitionProvider.scala:16)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$definition$1(ScalaPresentationCompiler.scala:386)
```
#### Short summary: 

scala.reflect.internal.FatalError: 
  unexpected tree: class scala.reflect.internal.Trees$Template
scala.AnyRef
     while compiling: file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
        during phase: globalPhase=<no phase>, enteringPhase=parser
     library version: version 2.13.12
    compiler version: version 2.13.12
  reconstructed args: -classpath <HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar -Ymacro-expand:discard -Ycache-plugin-class-loader:last-modified -Ypresentation-any-thread

  last tree to typer: Template
       tree position: line 66 of file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
              symbol: <none>
   symbol definition: <none> (a NoSymbol)
      symbol package: <none>
       symbol owners: 
           call site: <none> in <none>

== Source file context for tree position ==

    63 
    64     def waitForFinish() = {
    65 
    66         actors.forEachValue(1, actor: ActorRef => {
    67             actor.t
    68         })
    69         while (active.get() > 0) {