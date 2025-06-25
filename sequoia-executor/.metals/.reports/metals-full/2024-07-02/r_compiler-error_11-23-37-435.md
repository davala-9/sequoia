file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### java.lang.NullPointerException: Cannot invoke "scala.reflect.internal.Types$Type.typeSymbol()" because "tp" is null

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
offset: 2022
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

    def executeWithPartition(command: Runnable, partitionKey: String): Unit = {
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        actorRef.tell(command, actorRef)
    }

    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props.create(classOf[ExecutionServiceActor]), partitionKey)
    }

    def waitForFinish()@@


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
scala.reflect.internal.Definitions$DefinitionsClass.isByNameParamType(Definitions.scala:428)
	scala.reflect.internal.TreeInfo.isStableIdent(TreeInfo.scala:140)
	scala.reflect.internal.TreeInfo.isStableIdentifier(TreeInfo.scala:113)
	scala.reflect.internal.TreeInfo.isPath(TreeInfo.scala:102)
	scala.tools.nsc.interactive.Global.stabilizedType(Global.scala:974)
	scala.tools.nsc.interactive.Global.typedTreeAt(Global.scala:822)
	scala.meta.internal.pc.SignatureHelpProvider.signatureHelp(SignatureHelpProvider.scala:23)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$signatureHelp$1(ScalaPresentationCompiler.scala:332)
```
#### Short summary: 

java.lang.NullPointerException: Cannot invoke "scala.reflect.internal.Types$Type.typeSymbol()" because "tp" is null