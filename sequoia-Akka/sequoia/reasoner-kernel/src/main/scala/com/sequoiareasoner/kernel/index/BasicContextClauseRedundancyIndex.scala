/*
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This file is part of Sequoia, an OWL 2 reasoner that supports the SRIQ subset of OWL 2 DL.
 * Copyright 2017 by Andrew Bate <code@andrewbate.com>.
 *
 * This code is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 only,
 * as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License version 3 for more details (a copy is
 * included in the LICENSE file that accompanied this code).
 *
 * You should have received a copy of the GNU General Public License
 * version 3 along with this work.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * This file is available under and governed by the GNU General Public
 * License version 3 only, as published by the Free Software Foundation.
 * However, the following notice accompanied the original version of this
 * file:
 *
 * Copyright (c) 2016, Andrew Bate, University of Oxford <andrew.bate@cs.ox.ac.uk>.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the copyright holder nor the names of its contributors
 *       may be used to endorse or promote products derived from this software
 *       without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package com.sequoiareasoner.kernel.index

import com.sequoiareasoner.kernel.clauses._

/** A basic implementation of a context clause redundancy index that implements forward redundancy checking and
  * backward redundancy elimination.
  *
  * @author Andrew Bate <code@andrewbate.com>
  */
final class BasicContextClauseRedundancyIndex extends ContextClauseRedundancyIndex {


  private val literal2Long = new scala.collection.mutable.AnyRefMap[Literal,Long]()
  private var nextLong: Long = 1
  def getOrElseUpdate(l: Literal): Long = {
    literal2Long.getOrElseUpdate(l, {
      nextLong = nextLong + 1
      nextLong-1
    })
  }

  /** The clauses derived with an empty head **/
  private[this] val bottomClauses = new ArrayIndexedSequence[ContextClause](8, ArrayBuilders.contextClauseArrayBuilder)

  /** The clauses derived with a non-empty head. */
  private[this] val nonBottomClauses = new ArrayIndexedSequence[ContextClause](8, ArrayBuilders.contextClauseArrayBuilder)

  /** Map from a literal uid to the clauses in which that literal occurs (possibly non-maximally) in the head. */
  private[this] val headLiteralIndex = new LongIndexedSequenceMap[ContextClause](8, ArrayBuilders.contextClauseArrayBuilder)

  import com.sequoiareasoner.arrayops._

  override def add(clause: ContextClause): Unit =
    if (clause.head.length == 0) {
      bottomClauses += clause
    } else {
      nonBottomClauses += clause
      cforeach (clause.head) { l => headLiteralIndex.addBinding(getOrElseUpdate(l), clause) }
    }







  override def isClauseSubsumed(clause: ContextClause): Boolean = {
    val head: Array[Literal] = clause.head
    // Returns `true` iff `d` is subsumes or is equal to `clause`.
    def isSubsumingClause(d: ContextClause): Boolean = d.testStrengthening(clause) < 0
    /** Make sure that if the head of _clause_ is not empty, for each head literal L, get all clauses in the redundancy index
      * that contain L in the head, and check if each clause subsumes _clause_  */
    if (head.length > 0)
      cexists (head) { lit =>
        val candidatesToRemove: IndexedSequence[ContextClause] = headLiteralIndex(getOrElseUpdate(lit))
        candidatesToRemove.exists(isSubsumingClause)
      }
    else
      bottomClauses.exists(isSubsumingClause) || nonBottomClauses.exists(isSubsumingClause)
  }

  override def isClauseStrictlySubsumed(clause: ContextClause): Boolean = {
    val head: Array[Literal] = clause.head
    // Returns `true` iff `d` is subsumes `clause` but is not equal to `clause`.
    def isStrictlySubsumingClause(d: ContextClause): Boolean = clause.testStrengthening(d) > 0
    if (head.length > 0)
      cexists (head) { lit =>
        val candidatesToRemove: IndexedSequence[ContextClause] = headLiteralIndex(getOrElseUpdate(lit))
        candidatesToRemove.exists(isStrictlySubsumingClause)
      }
    else
      bottomClauses.exists(isStrictlySubsumingClause) || nonBottomClauses.exists(isStrictlySubsumingClause)
  }

  override def removeSubsumedClauses[U](clause: ContextClause)(f: ContextClause => Unit): Unit = {
    // remove requires that the collections support traversal and concurrent modification.
    def remove(clause: ContextClause): Unit =
      if (clause.head.length == 0) {
        bottomClauses -= clause
      } else {
        nonBottomClauses -= clause
        cforeach (clause.head) { l => headLiteralIndex.removeBinding(getOrElseUpdate(l), clause) }
      }
    val head: Array[Literal] = clause.head
    // Returns `true` iff `clause` is subsumes `d`.
    def isCandidateToRemove(d: ContextClause): Boolean = d.testStrengthening(clause) > 0
    if (head.length > 0) {
      cforeach (head) { lit =>
        val candidatesToRemove: IndexedSequence[ContextClause] = headLiteralIndex(getOrElseUpdate(lit))
        for (d <- candidatesToRemove)
          if (isCandidateToRemove(d)) { f(d); remove(d) }
      }
    } else {
      for (d <- bottomClauses) if (isCandidateToRemove(d)) { f(d); remove(d) }
      for (d <- nonBottomClauses) if (isCandidateToRemove(d)) { f(d); remove(d) }
    }
  }

  override def removeAllClauses[U](): Unit = {
    // remove requires that the collections support traversal and concurrent modification.
    def remove(clause: ContextClause): Unit =
      if (clause.head.length == 0) {
        bottomClauses -= clause
      } else {
        nonBottomClauses -= clause
      }
    for (clauseSet <- headLiteralIndex.valuesIterator; clause <- clauseSet) remove(clause)
    for (literal <- headLiteralIndex.keysIterator) headLiteralIndex.removeKey(literal)
  }

}
