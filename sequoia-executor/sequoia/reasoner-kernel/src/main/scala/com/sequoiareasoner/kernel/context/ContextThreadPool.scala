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

    def executeWithPartition(command: Runnable, c: ContextRunnable): Unit = {
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

