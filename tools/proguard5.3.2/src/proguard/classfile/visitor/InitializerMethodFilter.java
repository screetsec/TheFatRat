/*
 * ProGuard -- shrinking, optimization, obfuscation, and preverification
 *             of Java bytecode.
 *
 * Copyright (c) 2002-2016 Eric Lafortune @ GuardSquare
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */
package proguard.classfile.visitor;

import proguard.classfile.*;
import proguard.classfile.util.ClassUtil;

/**
 * This <code>MemberVisitor</code> delegates its visits to another given
 * <code>MemberVisitor</code>, but only to static initializers and instance
 * initializers.
 *
 * @author Eric Lafortune
 */
public class InitializerMethodFilter
implements   MemberVisitor
{
    private final MemberVisitor memberVisitor;


    /**
     * Creates a new InitializerMethodFilter.
     * @param memberVisitor the <code>MemberVisitor</code> to which visits
     *                      will be delegated.
     */
    public InitializerMethodFilter(MemberVisitor memberVisitor)
    {
        this.memberVisitor = memberVisitor;
    }


    // Implementations for MemberVisitor.

    public void visitProgramField(ProgramClass programClass, ProgramField programField) {}
    public void visitLibraryField(LibraryClass libraryClass, LibraryField libraryField) {}


    public void visitProgramMethod(ProgramClass programClass, ProgramMethod programMethod)
    {
        if (ClassUtil.isInitializer(programMethod.getName(programClass)))
        {
            memberVisitor.visitProgramMethod(programClass, programMethod);
        }
    }


    public void visitLibraryMethod(LibraryClass libraryClass, LibraryMethod libraryMethod)
    {
        if (ClassUtil.isInitializer(libraryMethod.getName(libraryClass)))
        {
            memberVisitor.visitLibraryMethod(libraryClass, libraryMethod);
        }
    }
}
