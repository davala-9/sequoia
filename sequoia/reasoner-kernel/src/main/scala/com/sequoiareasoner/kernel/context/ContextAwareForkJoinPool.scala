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

class ContextAwareForkJoinPool {
    val pool: ForkJoinPool = new ForkJoinPool()

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
            val c: Callable[Unit] = () => {
                task.call()
                context.setInactive()
            }
            pool.submit(c)
            // val r = pool.submit(task)
            // pullFromQueue(context)
            // r
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
