package com.sequoiareasoner.buildinfo

import scala.Predef._

/** This object was generated by sbt-buildinfo. */
case object BuildInfo {
  /** The value is "Sequoia Kernel". */
  val name: String = "Sequoia Kernel"
  /** The value is "0.6.1-alpha". */
  val version: String = "0.6.1-alpha"
  /** The value is "2.12.4". */
  val scalaVersion: String = "2.12.4"
  /** The value is 0. */
  val major: scala.Int = 0
  /** The value is 6. */
  val minor: scala.Int = 6
  /** The value is 1. */
  val patch: scala.Int = 1
  override val toString: String = {
    "name: %s, version: %s, scalaVersion: %s, major: %s, minor: %s, patch: %s" format (
      name, version, scalaVersion, major, minor, patch
    )
  }
}
