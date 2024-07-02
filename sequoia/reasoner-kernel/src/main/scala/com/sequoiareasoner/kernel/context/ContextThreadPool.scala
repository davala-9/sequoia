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


class ActorExecutionService extends ForkJoinPool {
    val actorSystem: ActorSystem = ActorSystem.create("context-actor-system")
    val actors: ConcurrentHashMap[String,ActorRef] = new ConcurrentHashMap()
    // val counter = new AtomicInteger(0)
    // val counterActor: ActorRef = actorSystem.actorOf(Props.create(classOf[CounterActor]), "counter")
    // val counterActor = actorSystem.actorOf(Props(new CounterActor), "counter")
    // implicit val timeout = Timeout(10, TimeUnit.MINUTES)

    def executeWithPartition(command: Runnable, c: ContextRunnable): Unit = {
        c.active = true
        val partitionKey = c.state.core.toString.replaceAll("[^a-zA-Z]", "")
        val actorRef: ActorRef = actors.computeIfAbsent(partitionKey, createNewActor(_))
        // counterActor.tell(1, actorRef)
        actorRef.tell(command, actorRef)
    }

    // private def createNewActor(partitionKey: String): ActorRef = {
    //     return actorSystem.actorOf(Props.create(classOf[ExecutionServiceActor]), partitionKey)
    // }
    private def createNewActor(partitionKey: String): ActorRef = {
        return actorSystem.actorOf(Props(new ExecutionServiceActor), partitionKey)
    }

    // def waitForFinish() = {
    //     // // Duration(10, MINUTES)
    //     var count: Int = 1
    //     // while (count != 0) {
    //     //     val countfuture: Future[Any] = counterActor ? 0
    //     //     count = Await.result(countfuture, timeout.duration).asInstanceOf[Int]
    //     //     // println("count: " + count)
    //     //     Thread.sleep(1000)
    //     // } // now need to sort out this bit
    //     while (count != 0) {
    //         count = actors.reduceValuesToInt(1, (actorRef: ActorRef) => {
    //             val countfuture: Future[Any] = actorRef ? 0
    //             Await.result(countfuture, timeout.duration).asInstanceOf[Int]
    //         })
    //         Thread.sleep(1000)
    //     }
    //     println("finito" + count + " , " + (count > 0).toString)
    // }
    
}

class ExecutionServiceActor extends Actor {
    // var counter = 0
    def receive: Receive = {
        case runnable: Runnable => {
            // counter = counter + 1
            runnable.run()
            // counter = counter - 1
        }
        // case 0 => sender() ! counter
        case m => throw new Exception(m.toString())
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

// class CounterActor extends Actor {
//     val counters = new ConcurrentHashMap[String, AtomicInteger]()
    
//     def receive: Receive = {
//         case 1 => {
//             val theSender = sender()
//             counters.computeIfAbsent(theSender.path.toString(), 0)
//             counters.get(theSender.path.toString()).incrementAndGet()
//         }
//         case -1 => {
//             val theSender = sender()
//             counters.computeIfAbsent(theSender.path.toString(), 0)
//             counters.get(theSender.path.toString()).decrementAndGet()
//         }
//         case 0 => {
//             val theSender = sender()
//             theSender ! counters.get()
//         }
//         case m => throw new Exception(m.toString())
//     }
// }

