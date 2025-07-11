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

package com.sequoiareasoner.kernel.taxonomy

import com.sequoiareasoner.kernel.owl.model.OWLObject

/** Represents sets of equivalent $OWLObjects with one canonical representative, and
  * refers to its sub- and super-nodes in a [[Taxonomy]].
  *
  * @author Andrew Bate <code@andrewbate.com>
  * @define OWLClass  [[com.sequoiareasoner.kernel.owl.model.OWLClass]]
  * @define OWLObject [[com.sequoiareasoner.kernel.owl.model.OWLObject]]
  */
trait TaxonomyNode[X <: OWLObject] {

//  /** Returns an immutable set of equivalent classes as imported IRIs.
//    *
//    * @return immutable set of equivalent classes as imported IRIs.
//    */
// def equivalentClasses: ImmutableIRISet

  def equivalentObjects: ImmutableIRISet

  /** Returns an unmodifiable set of nodes for OWLObjects that are direct super-objects of this Node.
    *
    * @return list of nodes for direct super-objects of this node's members.
    */
  def directSuperNodes: TaxonomyNodeSet[X]

  /** Returns an unmodifiable set of nodes for OWLObjects that are (possibly indirect) super-objects of members of this
    * Node. This is the smallest set of nodes that contains all direct super-nodes of this node, and all direct
    * super-nodes of every node in this set.
    *
    * @return set of nodes for sub-objects of this node's members.
    */
  def allSuperNodes: TaxonomyNodeSet[X]

  /** Returns an unmodifiable set of nodes for OWLObjects that are direct sub-objects of this TaxonomyNode.
    *
    * @return list of nodes for direct sub-objects of this node's members.
    */
  def directSubNodes: TaxonomyNodeSet[X]

  /** Returns an unmodifiable set of nodes for OWLObjects that are (possibly indirect) sub-objects of members of this
    * Node. This is the smallest set of nodes that contains all direct sub-nodes of this node, and all direct
    * sub-nodes of every node in this set.
    *
    * @return set of nodes for sub-objects of this node's members.
    */
  def allSubNodes: TaxonomyNodeSet[X]

}
