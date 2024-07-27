file://<WORKSPACE>/src/main/scala/com/sequoiareasoner/kernel/context/ContextAwareForkJoinPool.scala
### file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextAwareForkJoinPool.scala:43: error: `identifier` expected but `(` found
            context.queue.(task)
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
            val c: Callable[Unit] = () => { task.call(); context.setInactive() }
            pool.submit(c)
        } else { // if context is already active, queue the task to the context
            context.queue.(task)
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
	scala.meta.internal.parsers.ScalametaParser.syntaxErrorExpected(ScalametaParser.scala:387)
	scala.meta.internal.parsers.ScalametaParser.name(ScalametaParser.scala:1131)
	scala.meta.internal.parsers.ScalametaParser.termName(ScalametaParser.scala:1134)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$selector$1(ScalametaParser.scala:1190)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.selector(ScalametaParser.scala:1190)
	scala.meta.internal.parsers.ScalametaParser.simpleExprRest(ScalametaParser.scala:2129)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2074)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2041)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2038)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:1904)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1533)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1457)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$3(ScalametaParser.scala:4221)
	scala.meta.internal.parsers.ScalametaParser.stat(ScalametaParser.scala:4078)
	scala.meta.internal.parsers.ScalametaParser.iter$7(ScalametaParser.scala:4221)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1(ScalametaParser.scala:4234)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1$adapted(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:555)
	scala.meta.internal.parsers.ScalametaParser.blockStatSeq(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockOnBrace$2(ScalametaParser.scala:2366)
	scala.meta.internal.parsers.ScalametaParser.inBracesOnOpen(ScalametaParser.scala:259)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockOnBrace$1(ScalametaParser.scala:2364)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.blockOnBrace(ScalametaParser.scala:2364)
	scala.meta.internal.parsers.ScalametaParser.blockOnBrace(ScalametaParser.scala:2366)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockExprOnBrace$1(ScalametaParser.scala:2369)
	scala.meta.internal.parsers.ScalametaParser.blockExprPartial(ScalametaParser.scala:2348)
	scala.meta.internal.parsers.ScalametaParser.blockExprOnBrace(ScalametaParser.scala:2368)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2059)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2041)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2038)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:1904)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1533)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1457)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1374)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$ifClause$1(ScalametaParser.scala:1423)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:371)
	scala.meta.internal.parsers.ScalametaParser.ifClause(ScalametaParser.scala:1414)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1460)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:321)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:364)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1457)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$3(ScalametaParser.scala:4221)
	scala.meta.internal.parsers.ScalametaParser.stat(ScalametaParser.scala:4078)
	scala.meta.internal.parsers.ScalametaParser.iter$7(ScalametaParser.scala:4221)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1(ScalametaParser.scala:4234)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockStatSeq$1$adapted(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:555)
	scala.meta.internal.parsers.ScalametaParser.blockStatSeq(ScalametaParser.scala:4184)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockOnBrace$2(ScalametaParser.scala:2366)
	scala.meta.internal.parsers.ScalametaParser.inBracesOnOpen(ScalametaParser.scala:259)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockOnBrace$1(ScalametaParser.scala:2364)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:363)
	scala.meta.internal.parsers.ScalametaParser.blockOnBrace(ScalametaParser.scala:2364)
	scala.meta.internal.parsers.ScalametaParser.blockOnBrace(ScalametaParser.scala:2366)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$blockExprOnBrace$1(ScalametaParser.scala:2369)
	scala.meta.internal.parsers.ScalametaParser.blockExprPartial(ScalametaParser.scala:2348)
	scala.meta.internal.parsers.ScalametaParser.blockExprOnBrace(ScalametaParser.scala:2368)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2059)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2041)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2038)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:1904)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1533)
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

file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Freasoner-kernel%2Fsrc%2Fmain%2Fscala%2Fcom%2Fsequoiareasoner%2Fkernel%2Fcontext%2FContextAwareForkJoinPool.scala:43: error: `identifier` expected but `(` found
            context.queue.(task)
                          ^