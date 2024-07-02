file://<WORKSPACE>/sequoia/reasoner-kernel/src/main/scala/com/sequoiareasoner/kernel/context/ContextThreadPool.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:52: error: unclosed string literal
        println("count.value.get
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


class ActorExecutionService extends ForkJoinPool {
    val actorSystem: ActorSystem = ActorSystem.create("context-actor-system")
    val actors: ConcurrentHashMap[String,ActorRef] = new ConcurrentHashMap()
    // val counter = new AtomicInteger(0)
    // val counterActor: ActorRef = actorSystem.actorOf(Props.create(classOf[CounterActor]), "counter")
    val counterActor = actorSystem.actorOf(Props(new CounterActor), "counter")
    implicit val timeout = Timeout(10, TimeUnit.MINUTES)

    def executeWithPartition(command: Runnable, partitionKey: String): Unit = {
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        // counterActor.tell(1, actorRef)
        actorRef.tell(
            (() => command.run()): Runnable, 
            actorRef)
    }

    // private def createNewActor(partitionKey: String): ActorRef = {
    //     return actorSystem.actorOf(Props.create(classOf[ExecutionServiceActor]), partitionKey)
    // }
    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props(new ExecutionServiceActor), partitionKey)
    }

    def waitForFinish(): Future[Boolean] = {
        val count: Future[Any] = Await.result(counterActor ? 0, Duration(10, MINUTES))
        println("count.value.get
        while (count > 0) {
            println("counter" + count)
        } // now need to sort out this bit
        return true
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

// object CounterActor {
//   sealed trait Command
//   case class GiveMeCookies(count: Int, replyTo: ActorRef[Reply]) extends Command

//   sealed trait Reply
//   case class Cookies(count: Int) extends Reply
//   case class InvalidRequest(reason: String) extends Reply

//   def apply(): Behaviors.Receive[CookieFabric.GiveMeCookies] =
//     Behaviors.receiveMessage { message =>
//       if (message.count >= 5)
//         message.replyTo ! InvalidRequest("Too many cookies.")
//       else
//         message.replyTo ! Cookies(message.count)
//       Behaviors.same
//     }
// }

class CounterActor extends Actor {
    val counter = new AtomicInteger(0)
    
    def receive: Receive = {
        case 1 => counter.decrementAndGet()
        case -1 => counter.incrementAndGet()
        case 0 => {
            val theSender = sender()
            theSender ! counter.get()
        }
        case m => throw new Exception(m.toString())
    }
}


```



#### Error stacktrace:

```
scala.meta.internal.tokenizers.Reporter.syntaxError(Reporter.scala:23)
	scala.meta.internal.tokenizers.Reporter.syntaxError$(Reporter.scala:23)
	scala.meta.internal.tokenizers.Reporter$$anon$1.syntaxError(Reporter.scala:32)
	scala.meta.internal.tokenizers.Reporter.syntaxError(Reporter.scala:25)
	scala.meta.internal.tokenizers.Reporter.syntaxError$(Reporter.scala:25)
	scala.meta.internal.tokenizers.Reporter$$anon$1.syntaxError(Reporter.scala:32)
	scala.meta.internal.tokenizers.LegacyScanner.getStringLit(LegacyScanner.scala:509)
	scala.meta.internal.tokenizers.LegacyScanner.fetchDoubleQuote$1(LegacyScanner.scala:361)
	scala.meta.internal.tokenizers.LegacyScanner.fetchToken(LegacyScanner.scala:363)
	scala.meta.internal.tokenizers.LegacyScanner.nextToken(LegacyScanner.scala:201)
	scala.meta.internal.tokenizers.LegacyScanner.foreach(LegacyScanner.scala:912)
	scala.meta.internal.tokenizers.ScalametaTokenizer.uncachedTokenize(ScalametaTokenizer.scala:23)
	scala.meta.internal.tokenizers.ScalametaTokenizer.$anonfun$tokenize$1(ScalametaTokenizer.scala:17)
	scala.collection.concurrent.TrieMap.getOrElseUpdate(TrieMap.scala:962)
	scala.meta.internal.tokenizers.ScalametaTokenizer.tokenize(ScalametaTokenizer.scala:17)
	scala.meta.internal.tokenizers.ScalametaTokenizer$$anon$2.apply(ScalametaTokenizer.scala:322)
	scala.meta.tokenizers.Api$XtensionTokenizeDialectInput.tokenize(Api.scala:22)
	scala.meta.tokenizers.Api$XtensionTokenizeInputLike.tokenize(Api.scala:13)
	scala.meta.internal.parsers.ScannerTokens$.apply(ScannerTokens.scala:917)
	scala.meta.internal.parsers.ScalametaParser.<init>(ScalametaParser.scala:34)
	scala.meta.parsers.Parse$$anon$1.apply(Parse.scala:36)
	scala.meta.parsers.Api$XtensionParseDialectInput.parse(Api.scala:22)
	scala.meta.internal.semanticdb.scalac.ParseOps$XtensionCompilationUnitSource.toSource(ParseOps.scala:15)
	scala.meta.internal.semanticdb.scalac.TextDocumentOps$XtensionCompilationUnitDocument.toTextDocument(TextDocumentOps.scala:179)
	scala.meta.internal.pc.SemanticdbTextDocumentProvider.textDocument(SemanticdbTextDocumentProvider.scala:54)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$semanticdbTextDocument$1(ScalaPresentationCompiler.scala:462)
```
#### Short summary: 

file%3A%2F%2F%2Fhome%2Fpigeon%2FDownloads%2Fmsc%2FMSc-Project%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextThreadPool.scala:52: error: unclosed string literal
        println("count.value.get
                ^