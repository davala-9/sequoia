file://<WORKSPACE>/build.sbt
### file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Fbuild.sbt:112: error: illegal start of simple expression
      val AkkaVersion = "2.9.3"
      ^

occurred in the presentation compiler.

presentation compiler configuration:
Scala version: 2.13.12
Classpath:
<HOME>/.cache/coursier/v1/https/repo1.maven.org/maven2/org/scala-lang/scala-library/2.13.12/scala-library-2.13.12.jar [exists ]
Options:



action parameters:
uri: file://<WORKSPACE>/build.sbt
text:
```scala
import sbt._
import Keys._

//import CSOPlugin._

import RepeatCommandPlugin._


// [BEGIN] Fix for JavaDoc linking

import scala.util.matching.Regex
import scala.util.matching.Regex.Match

/*
 * The rt.jar file is located in the path stored in the sun.boot.class.path system property.
 * See the Oracle documentation at http://docs.oracle.com/javase/6/docs/technotes/tools/findingclasses.html.
 */
val rtJar: String = System.getProperty("sun.boot.class.path").split(java.io.File.pathSeparator).collectFirst {
  case str: String if str.endsWith(java.io.File.separator + "rt.jar") => str
}.get // fail hard if not found

val javaApiUrl: String = "http://docs.oracle.com/javase/8/docs/api/index.html"

def javadocLinkRegex(javadocURL: String): Regex = ("""\"(\Q""" + javadocURL + """\E)#([^"]*)\"""").r

val fixJavaLinks: Match => String = m =>
  m.group(1) + "?" + m.group(2).replace(".", "/") + ".html"

/**
 * You can print the classpath with `show compile:fullClasspath` in the SBT REPL.
 * From that list you can find the name of the jar for the managed dependency.
 *
 * @param externalJavadocMap  a map from managed dependency names to to the URLs of their respective Javadocs
 */
def documentationSettings(externalJavadocMap: Map[String, String] = Map.empty) = Seq(
  apiMappings ++= {
    // Lookup the path to jar from the classpath
    val classpath = (fullClasspath in Compile).value
    def findJar(nameBeginsWith: String): File = {
      classpath.find { attributed: Attributed[File] => (attributed.data ** s"$nameBeginsWith*.jar").get.nonEmpty }.get.data // fail hard if not found
    }
    // Define external documentation paths
    (externalJavadocMap map {
      case (name, javadocURL) => findJar(name) -> url(javadocURL)
    }) + (file(rtJar) -> url(javaApiUrl))
  },
  // Override the task to fix the links to JavaDoc
  doc in Compile ~= {
    target => {
      val allExternalJavadocLinks: Seq[String] = javaApiUrl +: externalJavadocMap.values.toSeq
      def hasJavadocLink(f: File): Boolean = allExternalJavadocLinks exists {
        javadocURL: String => 
          (javadocLinkRegex(javadocURL) findFirstIn IO.read(f)).nonEmpty
      }
      (target ** "*.html").get.filter(hasJavadocLink).foreach { f => 
        //println(s"Fixing $f.")
        val newContent: String = allExternalJavadocLinks.foldLeft(IO.read(f)) {
          case (oldContent: String, javadocURL: String) =>
            javadocLinkRegex(javadocURL).replaceAllIn(oldContent, fixJavaLinks)
        }
        IO.write(f, newContent)
      }
      target
    }
  }
)

// [END] Fix for JavaDoc linking

// commands += Command("betterPackage") { state: State => "clean" :: "set scalacOption in Compile += \"-Xdisable-assertions\"" :: "universal:packageBin" :: "session clear" :: state }

val licenseHeader =
  """|DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.

This file is part of Sequoia, an OWL 2 reasoner that supports the SRIQ subset of OWL 2 DL.
Copyright 2017 by Andrew Bate <code@andrewbate.com>.

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 only,
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License version 3 for more details (a copy is
included in the LICENSE file that accompanied this code).

You should have received a copy of the GNU General Public License
version 3 along with this work.  If not, see <http://www.gnu.org/licenses/>.
""".stripMargin

lazy val commonSettings = repeatCommandSettings ++ Seq(
  // version *must* be of the form MAJOR.MINOR.PATCH.BUILD where each component is an integer, otherwise String to Int parsing will fail.
  version      := "0.6.1-alpha",
  organization := "com.sequoiareasoner",
  scalaVersion := "2.12.4",
  scalacOptions ++= Seq("-opt:l:inline", "-opt-inline-from:**", "-deprecation", "-feature", "-Ydelambdafy:method", "-target:jvm-1.8", "-encoding", "UTF-8"),
  javacOptions ++= Seq("-source", "1.8", "-target", "1.8", "-Xlint:all"),
  //libraryDependencies += "com.typesafe" % "config" % "1.0.0",
  libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.4" % "test",
  // Useful test options:
  // D  Print the duration that a test takes to execute
  // F  Do not truncate stack traces in failed tests
  testOptions in Test += Tests.Argument("-oD"), 
  parallelExecution in Test := true,
  logBuffered in Test := false,
  autoAPIMappings := true,
  // Do not publish the documentation from each project since they need to link to each other. Use unidoc on the root instead.
  publishArtifact in packageDoc := false,
  headerLicense := Some(HeaderLicense.Custom(licenseHeader)),
  resolvers += "Akka library repository".at("https://repo.akka.io/maven"),
      val AkkaVersion = "2.9.3"
    libraryDependencies ++= Seq(
      "com.typesafe.akka" %% "akka-actor-typed" % AkkaVersion,
      "com.typesafe.akka" %% "akka-actor-testkit-typed" % AkkaVersion % Test
    )

  // Turn on the watchdog when running the tests
  //fork in Test := true,
  //javaOptions in Test ++= Seq("-Djava.system.class.loader=io.cso.watchdog.Loader", "-Dio.cso.watchdog.port=8080")
)

val OWLAPIVersion = "4.5.0"

// The OWL API should be a provided dependency and not included in the fat jar.
lazy val owlapiProvidedDependency = Seq(
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-api" % OWLAPIVersion % "provided",
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-apibinding" % OWLAPIVersion % "test",
)
lazy val owlapibindingProvidedDependency = Seq(
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-api" % OWLAPIVersion % "provided",
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-apibinding" % OWLAPIVersion % "provided",
)
lazy val owlapibindingNotProvidedDependency = Seq(
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-api" % OWLAPIVersion,
  libraryDependencies += "net.sourceforge.owlapi" % "owlapi-apibinding" % OWLAPIVersion,
)
lazy val loggingDependency = Seq(
  libraryDependencies += "org.slf4j" % "slf4j-api" % "1.7.22",
  libraryDependencies += "ch.qos.logback" % "logback-classic" % "1.2.3",
)
lazy val protegeDependency = Seq(
  libraryDependencies += "edu.stanford.protege" % "protege-editor-core" % "5.2.0" % "provided",
  libraryDependencies += "edu.stanford.protege" % "protege-editor-owl" % "5.2.0" % "provided",
)


lazy val externalJavadocMapForOwlApi = Map(
  // This should match the version of the OWL API above.
  "owlapi" -> "http://owlcs.github.io/owlapi/apidocs_4/index.html"
)

def isJarToEmbed(file: java.io.File): Boolean =
  file.getName match {
//    case name if name startsWith "cso" => true
    case name if name startsWith "jautomata" => true
    case name if name startsWith "scala" => true
    case name if name startsWith "balloontip" => true
    case _ => false
  }

lazy val osgiSettings = Seq(
  // Bundle-Version is set to the version by default.
  OsgiKeys.bundleSymbolicName := "com.sequoiareasoner.protege;singleton:=true",
  // Include the packages specified by privatePackage in the bundle.
  OsgiKeys.privatePackage := Seq("com.sequoiareasoner.*"),
  OsgiKeys.exportPackage := Seq("!*"),
  OsgiKeys.importPackage := Seq("!org.hamcrest","!sun.misc","*","sun.misc;resolution:=optional"),
  OsgiKeys.failOnUndecidedPackage := true,
  OsgiKeys.requireCapability := """osgi.ee;filter:="(&(osgi.ee=JavaSE)(version=1.8))"""",
  OsgiKeys.embeddedJars := (Keys.externalDependencyClasspath in Compile).value map (_.data) filter isJarToEmbed,
  OsgiKeys.additionalHeaders := Map(
    //"Update-Url" -> "http://update.sequoiareasoner.com/protege5.update.properties"
    "Update-Url" -> "http://localhost:8000/protege5.update.properties"
  )
)

/*
 * The id must match the id part of the Bundle-SymbolicName in the manifest file.
 * The version must be of the form used in the manifest file 'MAJOR.MINOR.PATCH[.qualifier]'.
 */
lazy val protegeUpdateProperties: String =
  """|id=com.sequoiareasoner.protege
version=0.6.2.alpha
name=Sequoia Reasoner
license=http://www.gnu.org/licenses/gpl-3.0.txt
readme=http://update.sequoiareasoner.com/VERSION/readme.html
download=http://update.sequoiareasoner.com/VERSION/file.jar
author=Andrew Bate <code@andrewbate.com>""".stripMargin

val pluginXMLTemplateName = "plugin.xml"

def versionParts(version: String, index: Int): Int = {
  val parts: Array[String] = version.takeWhile(c => c != '-' && c != '+').split("""\.""")
  assert(parts.length == 3, "Version must use Semantic Versioning format.")
  // Map all parts toInt to verify the syntax of the version number.
  (parts map {_.toInt}).apply(index)
}

// The default project on SBT startup is set in .sbtrc

lazy val macros        = (project in file("reasoner-macros")).
                          settings(commonSettings: _*).
                          settings(name := "Sequoia Macros").
                          settings(libraryDependencies += "org.scala-lang" % "scala-reflect" % scalaVersion.value)
                          disablePlugins(sbtassembly.AssemblyPlugin)

lazy val kernel        = (project in file("reasoner-kernel")).
                          settings(commonSettings ++ documentationSettings(): _*).
                          // settings(inConfig(Compile)(Seq(
                          //   manipulateBytecode := CSOPlugin.recompileHook.value
                          // )): _*).
                          // settings(inConfig(Test)(Seq(
                          //   manipulateBytecode := CSOPlugin.recompileHook.value
                          // )): _*).
                          enablePlugins(BuildInfoPlugin).
                          settings(
                            name := "Sequoia Kernel",
                            buildInfoKeys := Seq[BuildInfoKey](name, version, scalaVersion),
                            buildInfoKeys += "major" -> versionParts(version.value, 0),
                            buildInfoKeys += "minor" -> versionParts(version.value, 1),
                            buildInfoKeys += "patch" -> versionParts(version.value, 2),
                            buildInfoPackage := "com.sequoiareasoner.buildinfo"
                          ).
                          disablePlugins(sbtassembly.AssemblyPlugin).
                          dependsOn(macros)

lazy val owlapi        = (project in file("reasoner-owl-api")).
                          settings(commonSettings ++ documentationSettings(externalJavadocMapForOwlApi) ++ owlapiProvidedDependency: _*).
                          settings(name := "Sequoia OWL API Bindings",
                                   test in assembly := {}, // Skip tests in assembly.
                                   assemblyJarName in assembly := "Sequoia-OWL-API-fat-jar.jar",
                                   mainClass in assembly := None).
                          dependsOn(kernel % "compile->compile;test->test")

lazy val protegeplugin = (project in file("reasoner-protege-plugin")).
                          settings(commonSettings ++ documentationSettings() ++ protegeDependency ++ owlapibindingProvidedDependency: _*).
                          settings(name := "Sequoia Protege Plugin",
                                   resourceGenerators in Compile += Def.task {
                                     val template: java.io.File = sourceDirectory.value / "templates" / pluginXMLTemplateName
                                     val outfile: java.io.File = (resourceManaged in Compile).value / pluginXMLTemplateName
                                     val lines: Seq[String] = IO.readLines(template)
                                     val versionString: String = version.value
                                     val newLines = lines map { _.replaceAll("@@REASONER_NAME@@", s"Sequoia ($versionString)") }
                                     IO.writeLines(outfile, newLines)
                                     Seq(outfile)
                                   }.taskValue).
                          dependsOn(owlapi % "compile->compile;test->test").
                          disablePlugins(sbtassembly.AssemblyPlugin).
                          enablePlugins(SbtOsgi).
                          settings(osgiSettings: _*)

lazy val cli           = (project in file("reasoner-cli")).
                          settings(commonSettings ++ documentationSettings(externalJavadocMapForOwlApi) ++ owlapibindingNotProvidedDependency ++ loggingDependency: _*).
                          settings(name := "Sequoia Command-Line Interface",
                                   // Fix for "input line is too long" due to long classpath in bat on Windows.
                                   scriptClasspath := Seq("*"),
                                   // The executableScriptName should match the String in the main class to ensure that the documentation is correct.
                                   executableScriptName := "sequoia").
                          enablePlugins(JavaAppPackaging).
                          dependsOn(owlapi).
                          disablePlugins(sbtassembly.AssemblyPlugin)

// A aggregated root project is required for IntelliJ IDEA 2017.3 SBT imports.
lazy val root = (project in file(".")).aggregate(macros, kernel, owlapi, protegeplugin, cli)

```



#### Error stacktrace:

```
scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2276)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2230)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2227)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:2085)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1682)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1587)
	scala.meta.internal.parsers.ScalametaParser.argumentExpr(ScalametaParser.scala:2517)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$argumentExprsInParens$1(ScalametaParser.scala:2544)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$commaSeparated$1(ScalametaParser.scala:657)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$commaSeparated$1$adapted(ScalametaParser.scala:657)
	scala.meta.internal.parsers.ScalametaParser.iter$1(ScalametaParser.scala:647)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$tokenSeparated$1(ScalametaParser.scala:653)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$tokenSeparated$1$adapted(ScalametaParser.scala:640)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$listBy(ScalametaParser.scala:565)
	scala.meta.internal.parsers.ScalametaParser.tokenSeparated(ScalametaParser.scala:640)
	scala.meta.internal.parsers.ScalametaParser.commaSeparatedWithIndex(ScalametaParser.scala:660)
	scala.meta.internal.parsers.ScalametaParser.commaSeparated(ScalametaParser.scala:657)
	scala.meta.internal.parsers.ScalametaParser.argumentExprsInParens(ScalametaParser.scala:2544)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$getArgClauseOnParen$2(ScalametaParser.scala:2532)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$inParensAfterOpenOr(ScalametaParser.scala:252)
	scala.meta.internal.parsers.ScalametaParser.scala$meta$internal$parsers$ScalametaParser$$inParensOnOpenOr(ScalametaParser.scala:244)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$getArgClauseOnParen$1(ScalametaParser.scala:2533)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:316)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:365)
	scala.meta.internal.parsers.ScalametaParser.getArgClauseOnParen(ScalametaParser.scala:2533)
	scala.meta.internal.parsers.ScalametaParser.argClause$1(ScalametaParser.scala:2352)
	scala.meta.internal.parsers.ScalametaParser.simpleExprRest(ScalametaParser.scala:2353)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr0(ScalametaParser.scala:2278)
	scala.meta.internal.parsers.ScalametaParser.simpleExpr(ScalametaParser.scala:2230)
	scala.meta.internal.parsers.ScalametaParser.prefixExpr(ScalametaParser.scala:2227)
	scala.meta.internal.parsers.ScalametaParser.argumentExprsOrPrefixExpr(ScalametaParser.scala:2486)
	scala.meta.internal.parsers.ScalametaParser.getNextRhs$2(ScalametaParser.scala:2113)
	scala.meta.internal.parsers.ScalametaParser.getPostfixOrNextRhs$1(ScalametaParser.scala:2147)
	scala.meta.internal.parsers.ScalametaParser.loop$6(ScalametaParser.scala:2167)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:2192)
	scala.meta.internal.parsers.ScalametaParser.postfixExpr(ScalametaParser.scala:2087)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$expr$2(ScalametaParser.scala:1682)
	scala.meta.internal.parsers.ScalametaParser.atPosOpt(ScalametaParser.scala:319)
	scala.meta.internal.parsers.ScalametaParser.autoPosOpt(ScalametaParser.scala:366)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1587)
	scala.meta.internal.parsers.ScalametaParser.expr(ScalametaParser.scala:1486)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$patDefOrDcl$1(ScalametaParser.scala:3688)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:368)
	scala.meta.internal.parsers.ScalametaParser.autoEndPos(ScalametaParser.scala:373)
	scala.meta.internal.parsers.ScalametaParser.patDefOrDcl(ScalametaParser.scala:3675)
	scala.meta.internal.parsers.ScalametaParser.defOrDclOrSecondaryCtor(ScalametaParser.scala:3637)
	scala.meta.internal.parsers.ScalametaParser.nonLocalDefOrDcl(ScalametaParser.scala:3620)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$1.applyOrElse(ScalametaParser.scala:4479)
	scala.meta.internal.parsers.ScalametaParser$$anonfun$1.applyOrElse(ScalametaParser.scala:4474)
	scala.PartialFunction.$anonfun$runWith$1(PartialFunction.scala:231)
	scala.PartialFunction.$anonfun$runWith$1$adapted(PartialFunction.scala:230)
	scala.meta.internal.parsers.ScalametaParser.statSeqBuf(ScalametaParser.scala:4537)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$batchSource$13(ScalametaParser.scala:4771)
	scala.Option.getOrElse(Option.scala:201)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$batchSource$1(ScalametaParser.scala:4771)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:316)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:365)
	scala.meta.internal.parsers.ScalametaParser.batchSource(ScalametaParser.scala:4727)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$source$1(ScalametaParser.scala:4720)
	scala.meta.internal.parsers.ScalametaParser.atPos(ScalametaParser.scala:316)
	scala.meta.internal.parsers.ScalametaParser.autoPos(ScalametaParser.scala:365)
	scala.meta.internal.parsers.ScalametaParser.source(ScalametaParser.scala:4720)
	scala.meta.internal.parsers.ScalametaParser.entrypointSource(ScalametaParser.scala:4725)
	scala.meta.internal.parsers.ScalametaParser.parseSourceImpl(ScalametaParser.scala:135)
	scala.meta.internal.parsers.ScalametaParser.$anonfun$parseSource$1(ScalametaParser.scala:132)
	scala.meta.internal.parsers.ScalametaParser.parseRuleAfterBOF(ScalametaParser.scala:59)
	scala.meta.internal.parsers.ScalametaParser.parseRule(ScalametaParser.scala:54)
	scala.meta.internal.parsers.ScalametaParser.parseSource(ScalametaParser.scala:132)
	scala.meta.parsers.Parse$.$anonfun$parseSource$1(Parse.scala:29)
	scala.meta.parsers.Parse$$anon$1.apply(Parse.scala:36)
	scala.meta.parsers.Api$XtensionParseDialectInput.parse(Api.scala:25)
	scala.meta.internal.semanticdb.scalac.ParseOps$XtensionCompilationUnitSource.toSource(ParseOps.scala:17)
	scala.meta.internal.semanticdb.scalac.TextDocumentOps$XtensionCompilationUnitDocument.toTextDocument(TextDocumentOps.scala:206)
	scala.meta.internal.pc.SemanticdbTextDocumentProvider.textDocument(SemanticdbTextDocumentProvider.scala:54)
	scala.meta.internal.pc.ScalaPresentationCompiler.$anonfun$semanticdbTextDocument$1(ScalaPresentationCompiler.scala:403)
```
#### Short summary: 

file%3A%2F%2F%2Fhome%2Fpigeon%2Fparallel-sequoia%2Fsequoia%2Fbuild.sbt:112: error: illegal start of simple expression
      val AkkaVersion = "2.9.3"
      ^