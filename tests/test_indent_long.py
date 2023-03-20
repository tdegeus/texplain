import unittest

import texplain


class TestLatexIndentOneSentencePerLine(unittest.TestCase):
    """
    From https://github.com/cmhughes/latexindent.pl/tree/main/test-cases/oneSentencePerLine
    """

    def test_dbmrq(self):
        """
        Important difference: whitespace before and after commands is preserved.
        """

        text = r"""
A distinção entre conteúdo \emph{real} e conteúdo \emph{intencional} está
relacionada, ainda, à distinção entre o conceito husserliano de
\emph{experiência} e o uso popular desse termo. No sentido comum,
o \term{experimentado} é um complexo de eventos exteriores,
e o \term{experimentar} consiste em percepções (além de julgamentos e outros
atos) nas quais tais eventos aparecem como objetos, e objetos frequentemente
relacionados ao ego empírico. Nesse sentido, diz-se, por exemplo, que se
\term{experimentou} uma guerra. No sentido fenomenológico, no entanto,
é evidente que os eventos ou objetos externos não estão dentro do ego que os
experimenta, nem são seu conteúdo ou suas partes constituintes
\cite[5.][3]{lu}. Experimentar eventos exteriores, nesse sentido, significa
direcionar certos atos de percepção a tais eventos, de modo que certos
conteúdos constituem, então, uma unidade de consciência no fluxo unificado de
um ego empírico. Nesse caso, temos um todo \emph{real} do qual se pode dizer
que cada parte é de fato \emph{experimentada}. Enquanto no primeiro sentido há
uma distinção entre o conteúdo da consciência e aquilo que é experimentado
(e.g.\, entre a sensação e aquilo que é sentido), nesse último sentido aquilo
que o ego ou a consciência experimenta \emph{é} seu conteúdo.
        """

        formatted = r"""
A distinção entre conteúdo \emph{real} e conteúdo \emph{intencional} está relacionada, ainda, à distinção entre o conceito husserliano de
\emph{experiência} e o uso popular desse termo.
No sentido comum, o \term{experimentado} é um complexo de eventos exteriores, e o \term{experimentar} consiste em percepções (além de julgamentos e outros atos) nas quais tais eventos aparecem como objetos, e objetos frequentemente relacionados ao ego empírico.
Nesse sentido, diz-se, por exemplo, que se
\term{experimentou} uma guerra.
No sentido fenomenológico, no entanto, é evidente que os eventos ou objetos externos não estão dentro do ego que os experimenta, nem são seu conteúdo ou suas partes constituintes
\cite[5.][3]{lu}.
Experimentar eventos exteriores, nesse sentido, significa direcionar certos atos de percepção a tais eventos, de modo que certos conteúdos constituem, então, uma unidade de consciência no fluxo unificado de um ego empírico.
Nesse caso, temos um todo \emph{real} do qual se pode dizer que cada parte é de fato \emph{experimentada}.
Enquanto no primeiro sentido há uma distinção entre o conteúdo da consciência e aquilo que é experimentado (e.g.\, entre a sensação e aquilo que é sentido), nesse último sentido aquilo que o ego ou a consciência experimenta \emph{é} seu conteúdo.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_dbmrq3(self):
        """
        Important difference: whitespace before and after commands is preserved.
        """

        text = r"""
\some{
\mycommand{
\begin{something}
A distinção entre conteúdo \emph{real} e conteúdo \emph{intencional} está
relacionada, ainda, à distinção entre o conceito husserliano de
\emph{experiência} e o uso popular desse termo. No sentido comum,
o \term{experimentado} é um complexo de eventos exteriores,
e o \term{experimentar} consiste em percepções (além de julgamentos e outros
atos) nas quais tais eventos aparecem como objetos, e objetos frequentemente
relacionados ao ego empírico. Nesse sentido, diz-se, por exemplo, que se
\term{experimentou} uma guerra. No sentido fenomenológico, no entanto,
é evidente que os eventos ou objetos externos não estão dentro do ego que os
experimenta, nem são seu conteúdo ou suas partes constituintes
\cite[5.][3]{lu}. Experimentar eventos exteriores, nesse sentido, significa
direcionar certos atos de percepção a tais eventos, de modo que certos
conteúdos constituem, então, uma unidade de consciência no fluxo unificado de
um ego empírico. Nesse caso, temos um todo \emph{real} do qual se pode dizer
que cada parte é de fato \emph{experimentada}. Enquanto no primeiro sentido há
uma distinção entre o conteúdo da consciência e aquilo que é experimentado
(e.g.\, entre a sensação e aquilo que é sentido), nesse último sentido aquilo
que o ego ou a consciência experimenta \emph{é} seu conteúdo.
\end{something}
}
}
        """

        formatted = r"""
\some{
    \mycommand{
        \begin{something}
            A distinção entre conteúdo \emph{real} e conteúdo \emph{intencional} está relacionada, ainda, à distinção entre o conceito husserliano de
            \emph{experiência} e o uso popular desse termo.
            No sentido comum, o \term{experimentado} é um complexo de eventos exteriores, e o \term{experimentar} consiste em percepções (além de julgamentos e outros atos) nas quais tais eventos aparecem como objetos, e objetos frequentemente relacionados ao ego empírico.
            Nesse sentido, diz-se, por exemplo, que se
            \term{experimentou} uma guerra.
            No sentido fenomenológico, no entanto, é evidente que os eventos ou objetos externos não estão dentro do ego que os experimenta, nem são seu conteúdo ou suas partes constituintes
            \cite[5.][3]{lu}.
            Experimentar eventos exteriores, nesse sentido, significa direcionar certos atos de percepção a tais eventos, de modo que certos conteúdos constituem, então, uma unidade de consciência no fluxo unificado de um ego empírico.
            Nesse caso, temos um todo \emph{real} do qual se pode dizer que cada parte é de fato \emph{experimentada}.
            Enquanto no primeiro sentido há uma distinção entre o conteúdo da consciência e aquilo que é experimentado (e.g.\, entre a sensação e aquilo que é sentido), nesse último sentido aquilo que o ego ou a consciência experimenta \emph{é} seu conteúdo.
        \end{something}
    }
}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_dot_followed_by_tilde(self):
        text = r"""
Here is a sentence (Fig.~\ref{dummy18}). Here is another sentence (Fig.~\ref{dummy19}).
        """

        formatted = r"""
Here is a sentence (Fig.~\ref{dummy18}).
Here is another sentence (Fig.~\ref{dummy19}).
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_issue_321(self):
        text = r"""
\documentclass{article}

\begin{document}

I.e.\ it is a finite constant.

\end{document}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_issue_355(self):
        text = r"""
This is a very long sentence that I would like to be cut at the set line width which is however currently not done.
Sentences are put on different lines.
This is a very long sentence that is formatted like it should and it
should therefore not be touched by the formatter.
        """

        formatted = r"""
This is a very long sentence that I would like to be cut at the set line width which is however currently not done.
Sentences are put on different lines.
This is a very long sentence that is formatted like it should and it should therefore not be touched by the formatter.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_issue_376(self):
        text = r"""
For a slip event at interface $s$, we have $\Delta R_s > 0$ and $\Delta R_i = 0$ for $i \neq s$, inducing
\begin{equation}
    \label{eq:delta_fi}
    \Delta f_i = K\Delta R_s \,\, \mathrm{for} \,\, i \geq s ; \quad \Delta f_i=0 \,\, \mathrm{otherwise}.
\end{equation}
We can then deduce that
\begin{equation}
    \label{eq:DR_DF_multi}
    \Delta F = \frac{h K}{H} \Delta R_s \sum\limits_{i=s}^n i \, = \frac{h K}{H}\Delta R_s (n+s)(n-s+1) / 2.
\end{equation}
which we verify in \cref{fig:2c}.
        """

        formatted = r"""
For a slip event at interface $s$, we have $\Delta R_s > 0$ and $\Delta R_i = 0$ for $i \neq s$, inducing
\begin{equation}
    \label{eq:delta_fi}
    \Delta f_i = K\Delta R_s \,\, \mathrm{for} \,\, i \geq s ; \quad \Delta f_i=0 \,\, \mathrm{otherwise}.
\end{equation}
We can then deduce that
\begin{equation}
    \label{eq:DR_DF_multi}
    \Delta F = \frac{h K}{H} \Delta R_s \sum\limits_{i=s}^n i \, = \frac{h K}{H}\Delta R_s (n+s)(n-s+1) / 2.
\end{equation}
which we verify in \cref{fig:2c}.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_issue_392(self):
        r"""
        Difference with ``latexindent.pl``: abbrivations not automatically recognized.
        Instead use ``"~"`` or ``"\ "`` to have a space after the abbreviation.
        """

        text = r"""
\section{e.G. example}
some text with. e.G.~A sentence.

\section{E.G. example}
some text with. e.G.\ A sentence.

\subsection{Ph.D. example}
other text. Ph.D.\ With sentences.
        """

        formatted = r"""
\section{e.G. example}
some text with.
e.G.~A sentence.

\section{E.G. example}
some text with.
e.G.\ A sentence.

\subsection{Ph.D. example}
other text.
Ph.D.\ With sentences.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_kiryph1(self):
        """
        Difference: comment left in place.
        """

        text = r"""
Xx xxxxxxxx, xxx xxxxxxxx xxxxxxxxxx, xxxxxxxxxx xxxxxxxxxxx xxxxxxxx xx x
 xxxxxxxx xx xxxx xx xxxxxxx \enquote{xxxxxx xxxx xxxxxxxxx}%
  \cite{XxxxxXxXx:xxxx}.
 Xxxx x xxxxxxxx xx xxxxxx \emph{xxxxxxx} \cite{XxxxxXxXx:xxxx} xxx xx
   xxxxxxxx xxxxxxxxxxxxx xx x xxxxxxxx \emp{Xxxxxxx'x xxxxx}.
        """

        formatted = r"""
Xx xxxxxxxx, xxx xxxxxxxx xxxxxxxxxx, xxxxxxxxxx xxxxxxxxxxx xxxxxxxx xx x xxxxxxxx xx xxxx xx xxxxxxx \enquote{xxxxxx xxxx xxxxxxxxx}%
\cite{XxxxxXxXx:xxxx}.
Xxxx x xxxxxxxx xx xxxxxx \emph{xxxxxxx} \cite{XxxxxXxXx:xxxx} xxx xx xxxxxxxx xxxxxxxxxxxxx xx x xxxxxxxx \emp{Xxxxxxx'x xxxxx}.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_konfect(self):
        text = r"""
The filter does different things depending on the file format;
  in most cases
  it is determined on the output of the "file" command [2], [6], that recognizes
  lots of formats.

C'est bon; à six
heures on y va.
        """

        formatted = r"""
The filter does different things depending on the file format; in most cases it is determined on the output of the "file" command [2], [6], that recognizes lots of formats.

C'est bon; à six heures on y va.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_mlep(self):
        r"""
        Difference with ``latexindent.pl``: abbrivations not automatically recognized.
        Instead use ``"~"`` or ``"\ "`` to have a space after the abbreviation.
        """

        text = r"""
This is an example (i.e.~a test).  The unit is $\rm kg.m^{-2}.s^{-1}$.  Values goes from 0.02 to 0.74 Pa.  Here some space needed \hspace{0.5cm}.  The value is $\lambda=3.67$.  The URL is \url{www.scilab.org}.
        """

        formatted = r"""
This is an example (i.e.~a test).
The unit is $\rm kg.m^{-2}.s^{-1}$.
Values goes from 0.02 to 0.74 Pa.
Here some space needed \hspace{0.5cm}.
The value is $\lambda=3.67$.
The URL is \url{www.scilab.org}.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_mlep2(self):
        text = r"""
The names (Smith, Doe, etc.) are inherited.

Two items are used:
\begin{itemize}
    \item Item 1.
    \item Item 2.
\end{itemize}

The energy is defined as
\begin{equation}
    E=m c^2
\end{equation}
where m is the mass.

\begin{table}[htbp]
    \caption{\label{tab1} Here is the legend.}
    \begin{tabular}{cc}
        1 & 1 \\
    \end{tabular}
\end{table}

This is a sentence.

\begin{table}[htbp]
    \caption{\label{tab1} Here is the legend.}
    \begin{tabular}{cc}
        1 & 1 \\
    \end{tabular}
\end{table}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_more_code_blocks(self):
        text = r"""
\section*{Executive Summary}
Sonifications are non-verbal representation of plots or graphs.
This report details the results of an eSTEeM-funded project
to investigate the efficacy of sonifications when presented to
participants in study-like activities. We are grateful to eSTEeM
for their support and funding throughout the project.

\tableofcontents
\section{Introduction}
The depiction of numerical data using graphs and charts play a vital part in many STEM modules.  As Tufte says in a key text about the design of plots and charts ``at their best graphics are instruments for reasoning about quantitative measurement'' \cite{Tufte1983}. In this report we will focus on static images, such as graphs and plots in printed materials. Dynamic images in which the user can change
features of the diagram or graph are not considered.  In order to meet the OU's mission of being open to [all] people, such plots and graphs need to be accessible to \emph{all} students, as some students may otherwise be disadvantaged in their study.

The Equality Act 2010 \cite{ehrcequalityact} requires universities to avoid discrimination against people with protected characteristics,
including disability, and to do so by making `reasonable adjustments'. The Equality and Human Rights Commission offers guidance
for Higher Education providers \cite{ehrcprovidersguidance}. The Act created the Public Sector Equality Duty \cite{ehrcpublicsector}, which
requires universities to promote equality of opportunity by removing disadvantage and meet the needs of protected groups.
In the context of The Open University, this means that the authors of module materials should ensure that plots and charts (or alternate versions of them) are accessible to all students with visual impairments, including those students with no vision at all.

Individuals who are blind have often had limited access to mathematics and science \cite{advisorycommission},
especially in distance learning courses \cite{educause}; in part this is because of the highly visual nature of the representations of numerical relationships. Methods commonly used to accommodate learners who are blind or have low vision include: use of sighted assistants who can describe graphics verbally; provision of text-based descriptions of graphics that can be read with text-to-speech applications (for example JAWS \cite{jaws}, Dolphin \cite{dolphin}); accessed as Braille, either as hard copy or via refreshable display, or through provision of tactile graphics for visual representations.

Desirable features of an accessible graph include the following \cite{Summers2012}:
\begin{itemize}
 \item Perceptual precision: the representation allows the user to interpret the plot with an appropriate amount of detail.
 \item First-hand access: the representation allows the user to directly interpret the data and is not reliant on subject interpretation by others (bias).
 \item Works on affordable, mainstream hardware.
 \item Born-accessible: the creator of the plot would not have to put extra effort into creating the accessible version.
\end{itemize}

\begin{figure}[!htb]
 \centering
  \figureDescription{Screenshot of participant S7 interacting with the ferris wheel example.}
 \includegraphics[width=.5\textwidth]{p7-ferris-wheel}
 \caption{Visualisation of the sonification from S7.}
 \label{fig:partipants-ferris-wheel}
\end{figure}
        """

        formatted = r"""
\section*{Executive Summary}
Sonifications are non-verbal representation of plots or graphs.
This report details the results of an eSTEeM-funded project to investigate the efficacy of sonifications when presented to participants in study-like activities.
We are grateful to eSTEeM for their support and funding throughout the project.

\tableofcontents
\section{Introduction}
The depiction of numerical data using graphs and charts play a vital part in many STEM modules.
As Tufte says in a key text about the design of plots and charts ``at their best graphics are instruments for reasoning about quantitative measurement'' \cite{Tufte1983}.
In this report we will focus on static images, such as graphs and plots in printed materials.
Dynamic images in which the user can change features of the diagram or graph are not considered.
In order to meet the OU's mission of being open to [all] people, such plots and graphs need to be accessible to \emph{all} students, as some students may otherwise be disadvantaged in their study.

The Equality Act 2010 \cite{ehrcequalityact} requires universities to avoid discrimination against people with protected characteristics, including disability, and to do so by making `reasonable adjustments'.
The Equality and Human Rights Commission offers guidance for Higher Education providers \cite{ehrcprovidersguidance}.
The Act created the Public Sector Equality Duty \cite{ehrcpublicsector}, which requires universities to promote equality of opportunity by removing disadvantage and meet the needs of protected groups.
In the context of The Open University, this means that the authors of module materials should ensure that plots and charts (or alternate versions of them) are accessible to all students with visual impairments, including those students with no vision at all.

Individuals who are blind have often had limited access to mathematics and science \cite{advisorycommission}, especially in distance learning courses \cite{educause}; in part this is because of the highly visual nature of the representations of numerical relationships.
Methods commonly used to accommodate learners who are blind or have low vision include: use of sighted assistants who can describe graphics verbally; provision of text-based descriptions of graphics that can be read with text-to-speech applications (for example JAWS \cite{jaws}, Dolphin \cite{dolphin}); accessed as Braille, either as hard copy or via refreshable display, or through provision of tactile graphics for visual representations.

Desirable features of an accessible graph include the following \cite{Summers2012}:
\begin{itemize}
    \item Perceptual precision: the representation allows the user to interpret the plot with an appropriate amount of detail.
    \item First-hand access: the representation allows the user to directly interpret the data and is not reliant on subject interpretation by others (bias).
    \item Works on affordable, mainstream hardware.
    \item Born-accessible: the creator of the plot would not have to put extra effort into creating the accessible version.
\end{itemize}

\begin{figure}[!htb]
    \centering
    \figureDescription{Screenshot of participant S7 interacting with the ferris wheel example.}
    \includegraphics[width=.5\textwidth]{p7-ferris-wheel}
    \caption{Visualisation of the sonification from S7.}
    \label{fig:partipants-ferris-wheel}
\end{figure}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_multiple_sentences9(self):
        text = r"""
This paragraph% first comment
has line breaks throughout its paragraph;% second comment
we would like to combine% third comment
the textwrapping% fourth comment
and paragraph removal routine. % fifth comment
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), text.strip())

    def test_other_begins(self):
        text = r"""
This is the first
sentence. 7 is the second
sentence. This is the
third sentence.

This is the fourth
sentence! This is the fifth sentence? This is the
sixth sentence. $a$ is often
referred to as
an integer. furthermore
we have that.
        """

        formatted = r"""
This is the first sentence.
7 is the second sentence.
This is the third sentence.

This is the fourth sentence!
This is the fifth sentence?
This is the sixth sentence.
$a$ is often referred to as an integer.
furthermore we have that.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_pcc_program_review1(self):
        text = r"""
% arara: pdflatex: {files: [MathSACpr2014]}
% !arara: indent: {overwrite: yes}
\chapter{Facilities and Support}
\begin{flushright}
    \includegraphics[width=8cm]{xkcd-806-tech_support-punchline}\\
    \url{http://xkcd.com}
\end{flushright}
\section[Space, technology, and equipment]{Describe how classroom space, classroom technology, laboratory space
and equipment impact student success.}

Over the past few years, efforts by the college to create classrooms containing
the same basic equipment has helped tremendously with consistency issues.  The
nearly universal presence of classroom podiums with attendant Audio Visual (AV) devices is
considerably useful.  For example, many instructors use computer-based
calculator emulators when instructing their students on calculator use---this
allows explicit keystroking examples to be demonstrated that were not possible
before the podiums appeared; the document cameras found in most classrooms are
also used by most mathematics instructors.     Having an instructor computer with
internet access has been a great help as instructors have access to a wide
variety of tools to engage students, as well as a source for quick answers when
unusual questions arise.

Several classrooms on the Sylvania campus have Starboards  or Smart Boards
integrated with their AV systems.  Many mathematics instructors use these tools
as their primary presentation vehicles;  documents can be preloaded into the
software and the screens allow instructors to write their work directly onto
the document.  Among other things, this makes it easy to save the work into pdf
files that can be accessed by students outside of class.  This equipment is not
used as much on the other campuses, but there are instructors on other campuses
that say they would use them if they were widely available on their campus.

A few instructors have begun creating lessons with LiveScribe technology.  The
technology allows the instructor to make an audio/visual record of their
lecture without a computer or third person recording device; instructors can
post a `live copy' of their actual class lecture online.  The students  do not
simply see a static copy of the
notes that were written;  the students see the notes emerge as they were being
written and they hear the words that were spoken while they were written.  The
use of LiveScribe technology is strongly supported by Disability Services, and
for that reason alone continued experimentation with its use is strongly
encouraged.

Despite all of the improvements that have been made in classrooms over the past
few years, there still are some serious issues.

Rooms are assigned randomly, which often leads to mathematics classes being
scheduled in rooms that are not appropriate for a math class. For example,
scheduling a math class in a room with individual student desks creates a lot
of problems; many instructors have students take notes, refer to their text,
and use their calculator all at the same time and there simply is not enough
room on the individual desktops to keep all of that material in place.  More
significantly,  this furniture is especially ill-suited for group work.  Not
only does the movement of desks and sharing of work exacerbate the materials
issue (materials frequently falling off the desks), students simply cannot
share their work in the efficient way that work can be shared when they are
gathered about tables.  It would be helpful if all non-computer-based math
classes could be scheduled in rooms with tables.

Another problem relates to an inadequate number of computerized classrooms and
insufficient space in many of the existing computerized classroom;  both of
these shortages have greatly increased due to Bond-related construction.
Several sections of MTH 243 and MTH 244 (statistics courses), which are
normally taught in computerized classrooms, \emph{have} been scheduled in regular
classrooms.  Many of the statistics courses that were scheduled in
computerized classrooms have been scheduled in rooms that seat only 28, 24, or
even 20 students.  When possible, we generally limit our class capacities at 34
or 35.  Needless to say, running multiple sections of classes in rooms well
below those capacities creates many problems.  This is especially  problematic
for student success, as it hinders students'  ability to register due to
undersized classrooms.

Finally, the computerized classrooms could be configured in such a way that
maximizes potential for meaningful student engagement and minimizes potential
for students to get off course due to internet access.  We believe that all
computerized classrooms need to come equipped with software that allows the
instructor control of the student computers such as LanSchool Classroom
Management Software.   The need for this technology is dire; it will reduce or
eliminate students being off task when using computers, and it will allow
another avenue to facilitate instruction as the instructor will be able to
`see' any student computer and `interact' with any student computer.  It can
also be used to solicit student feedback in an anonymous manner.  The gathering
of anonymous feedback can frequently provide a better gauge of the general
level of understanding than activities such as the traditional showing of
hands.

\recommendation[Scheduling]{All mathematics classes should be scheduled in rooms that are either
    computerized (upon request) or have multi-person tables (as opposed to
individual desks).}

\recommendation[Scheduling, Deans of Instruction, PCC Cabinet]{All computerized classrooms
    should have at least 30, if not 34, individual work
stations.}

\recommendation[Multimedia Services, Deans of Instruction, PCC Cabinet]{An adequate number of classrooms on all campuses should be equipped with
    Smartboards so that all instructors who want access to the technology can teach
every one of their classes in rooms equipped with the technology.}

\recommendation[Multimedia Services, TSS]{The disk image for all computerized classrooms should include software that
    allows the podium computer direct access to each student
computer. }

\section[Library and other outside-the-classroom information
resources]{Describe how students are using the library or other
outside-the-classroom information resources.  }
We researched this topic by conducting a stratified sampling method
survey of 976 on-campus students and 291 online students; the participants were
chosen in a random manner.  We gave scantron surveys to the on-campus students
and used SurveyMonkey for the online students. We found that students are
generally knowledgeable about library resources and other outside-the-classroom
resources.  The complete survey, together with its results, is given in
\vref{app:sec:resourcesurvey}; we have summarized our comments to some of the
more interesting questions below.

\begin{enumerate}[label=Q\arabic*.,font=\bf]
    \item Not surprisingly, library resources and other campus-based resources
    are used more frequently by our on-campus students than by our online
    students. This could be due to less frequent visits to campus for online
    students and/or online students already having similar resources available
    to them via the internet.
    \item We found that nearly 70\% of instructors include resource information
    in their syllabi.  This figure was consistent regardless of the level of
    the class (DE/transfer level) or the employment status of the instructor
    (full/part-time).

    We found that a majority of our instructors are using online resources to
    connect with students. Online communication between students and
    instructors is conducted across many platforms such as instructor websites,
    Desire2Learn, MyPCC, online graphing applications, and online homework
    platforms.

    We found that students are using external educational websites such as
    \href{https://www.khanacademy.org/}{Khan Academy},
    \href{http://patrickjmt.com/}{PatrickJMT},
    \href{http://www.purplemath.com/}{PurpleMath}, and
    \href{http://www.youtube.com/}{YouTube}.  The data suggest online
    students use these services more than on-campus students.
    \item The use of online homework (such as WeBWorK,  MyMathLab, MyStatLab, and
    ALEKS) has grown significantly over the past few years. However, the data
    suggests that significantly more full-time instructors than part-time
    instructors are directing their students towards these tools (as either a
    required or optional component of the course).  Additionally, there is a
    general trend that online homework programs are being used more frequently
    in online classes than in on-campus classes.  Both of these discrepancies
    may reflect the need to distribute more information to faculty about these
    software resources.
    \item The Math SAC needs to address whether or not we should be requiring
    students to use online resources that impose additional costs upon the
    students and, if so, what would constitute a reasonable cost to the
    student.  To that end, our survey asked if students would be willing to pay
    up to \$35 to access online homework and other resources.   We found that
    online students were more willing to pay an extra fee than those enrolled
    in on-campus classes.
    \setcounter{enumi}{6}
    \item The PCC mathematics website offers a wealth of materials that are
    frequently accessed by students. These include course-specific supplements,
    calculator manuals, and the required Calculus I lab manual; all of these
    materials were written by PCC mathematics faculty.  Students may print
    these materials for free from any PCC computer lab. The website also links
    to PCC-specific information relevant to mathematics students (such as
    tutoring resources) as well as outside resources (such as the Texas
    Instruments website).
    \setcounter{enumi}{8}
    \item In addition to the previously mentioned resources we also encourage
    students to use resources offered at PCC such as on-campus Student Learning
    Centers, online tutoring, Collaborate, and/or Elluminate. A significant
    number of students registered in on-campus sections are using these
    resources whereas students enrolled in online sections generally are not.
    This is not especially surprising since on-campus students are, well, on
    campus whereas many online students rarely visit a campus.
\end{enumerate}

\recommendation[Math SAC]{The majority of our data suggests that students are using a variety of
    resources to further their knowledge. We recommend that instructors continue to
    educate students about both PCC resources and non-PCC resources. We need to
    uniformly encourage students to use resources such as online tutoring, Student
    Learning Centers, Collaborate, and/or Elluminate; this includes resource
citations in each and every course syllabus.}

\recommendation[Faculty Department Chairs]{A broader education campaign should be engaged to distribute information to
    part-time faculty regarding online homework such as WeBWorK, MyMathLab,
MyStatLab, and ALEKS. }

\recommendation[Math SAC]{Instructors should consider quality, accessibility and cost to students when
requiring specific curriculum materials. }

\section[Clerical, technical, administrative and/or tutoring support]{Provide
information on clerical, technical, administrative and/or tutoring support.}

The Math SAC has a sizable presence on each of PCC's three campuses and at Southeast Center (soon to be
a campus in its own right). Each campus houses a math department within a
division of that campus. The clerical, technical, administrative, and tutoring
support systems are best described on location-by-location basis.

\subsection{Clerical, technical, and administrative support}

Across the district, our SAC has an excellent and very involved administrative
liaison, Dr. Alyson Lighthart. We would like to thank her for her countless
hours of support in attending our SAC meetings and being available to the SAC
Co-Chairs. She provides us with thoughtful feedback and insightful perspectives
that help us gather our thoughts and make sound decisions.

\subsubsection{Cascade}
The Cascade math department belongs to the Math, Sciences, Health and PE
division. The math department is located on the third floor of the student
services building, sharing a floor with the ROOTS office. The math department
also shares space with allied health support staff, medical professions
faculty, medical assisting faculty and the Cascade academic intervention
specialists (one of whom is also a math part-time faculty).  Part-time math
faculty share 11 cubicles, each with a computer. Our 7 full-time instructors
are paired in offices that open up to the part-time cubicles. We have space in
our offices for another full time faculty member as we lost a temporary
full-time position at the start of the 2013 academic year. In Winter 2014, a
collective 42 faculty share one high speed Ricoh printer and one copy machine.
Our division offices are located in another building. We have a dedicated
administrative assistant at the front desk who helps students and faculty most
days from 8 {\sc a.m.--5 p.m.}

\subsubsection{Rock Creek}
The Rock Creek math department is located in the same floor as the division it
belongs to (Mathematics, Aviation, and Industrial Technology) and it is shared
with Computer Science.   Part-time faculty share fourteen cubicles, each with a
computer, located in the same office as full-time instructors, that are used to
prepare and meet with students. The sixty-five plus faculty share two high
speed printers that can collate, staple and allow double sided printing, and
one high speed scanner. Currently we have reached space capacity and we will
have to re-think the current office configuration in order to add one more
full-time faculty member next Fall.  Two years ago the Rock Creek math
department added a dedicated administrative assistant, which has helped with
scheduling needs, coordinating part-time faculty needs, and providing better
service to the students.

\subsubsection{Southeast}
The clerical and administrative setup at Southeast has changed, as of Winter
2014. There was a recent restructuring of divisions. What used to be the
Liberal Arts and Sciences Division split into two divisions: the Liberal Arts
and CTE Division (which is in the first floor of Scott Hall, Room 103, where
the Liberal Arts and Sciences used to be) and the Math and Science Division
(which is on the \nth{2} floor of the new Student Commons Building, Room 214).
All of the math and science faculty are now in this new space, including the
part-time instructors (everybody was scattered before, so this is a welcome
change).

All of the department chairs have their own offices (with doors), while the
rest of the faculty (full-time and part-time) occupy cubicle spaces
(approximately 20 cubicles in the space, shared by 4--5 faculty per cubicle).
There are two administrative assistants, one of whom is with the math and
science faculty and the other of whom is in charge of the STEM program.  There
is also one clerical staff member.

There is one Ricoh printer in the space, along with a fax machine.  Any and all
supplies (markers, erasers, etc.) are located across the hall in a designated
staff room.

\subsubsection{Sylvania}
The Sylvania math department belongs to the Math and Industrial Technology
division, which is located in the neighboring automotive building.  The math
department is currently located in two separate areas of adjacent buildings as
of Fall 2013, when the developmental math faculty officially merged with the
math department.  This separation will soon be remedied by construction of the
new math department area, scheduled to be completed during Spring 2014.  This
new location will be next door to the Engineering department, and will share a
conference room, copy machine room, and kitchen. The math department will
include two department chair offices, seventeen full-time instructor cubicles,
six additional cubicles shared by part-time faculty, and two flex-space rooms.
Each of the cubicles will have a computer, and there will be two shared laser
printers plus one color scanner in the department office.

Our two administrative assistants work an overlapped schedule, which provides
dual coverage during the busy midday times and allows the office to remain
open to students and visitors for eleven hours.  These assistants do an
incredible job serving both student and faculty needs, including:  scheduling
assistance, interfacing with technical support regarding office and classroom
equipment, maintaining supplies inventory, arranging for substitute
instructors, securing signatures and processing department paperwork, guiding
students to campus resources, and organizing syllabi and schedules from
approximately 70 math instructors.

Our math department has frequent interaction with both Audio-Visual and
Technology Solution Services.  Responses by AV to instructor needs in the
classroom are extremely prompt--typically within minutes of the notification of
a problem.  Since the math department is very technology-oriented, we have many
needs that require the assistance of TSS.  Work orders for computer equipment
and operational issues that arise on individual faculty computers can take
quite a long time to be implemented or to be resolved.  This may be due to the
sheer volume of requests that they are processing, but more information during
the process, especially notes of any delays, would be welcomed.

\subsection{Tutoring support}
PCC has a Student Learning Center (SLC) on each campus.  It is a
testament to PCC's commitment to student success that the four SLCs exist.
However, discrepancies such as unequal distribution of resources, inconsistency
in the number and nature of tutors (including faculty `donating time' to the
centers), and disparate hours
of operation present challenges to students trying to navigate their way
through different centers.

\recommendation[PCC Cabinet, Deans of Students, Deans of Instructions, Student Learning Centers]{The college should strive for more
    consistency with its Student Learning Centers. We feel that the centers would
    be an even greater resource if they were more consistent in structure, resource
availability, physical space, and faculty support.}

Over the last five years the general environment of PCC has been greatly
impacted by historically-unmatched enrollment growth (see
\vref{fig:sec3:DLenrollments,fig:sec3:F2Fenrollments}). PCC's four Student
Learning Centers have been greatly affected by this (see \vref{app:sec:tutoringhours}).
Most notably, the number of students seeking math tutoring has
increased dramatically.  Unfortunately, this increase in student need has not
been met by increase in tutors or tutoring resources.  As a result the
amount of attention an individual student receives has decreased in a
substantive way, leaving students often frustrated and without the help they
needed. Consequently, the numbers of students dropped again as students stopped
even trying.   While some of this growth has been (or will be) accommodated
by increasing the physical space available for tutoring (i.e., by the
construction of new facilities at Rock Creek and Southeast),
that is still not enough since personnel resources were not increased at the
same rate and work-study awards have been decreased significantly.  A
comprehensive plan needs to be developed and implemented that will ensure each
and every student receives high-quality tutoring in a consistent and
consistently accessible manner.

As it now stands, the operation of the SLCs is completely campus driven.  As
such, reporting on the current status needs to be done on a campus-by-campus
basis.

\subsubsection{Cascade}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Cascade SLC has served about
680 math students with 3900 individual visits and 8 hours per student per term.
(See \vref{app:tut:tab:SLC} for a full accounting.)

The Cascade SLC has increased its operating hours in response to student
demand. Statistics tutoring is now offered at most times and the introduction of
online homework has led to `Hybrid Tutoring', where students receive tutoring
while working on their online homework.

At the Cascade Campus, all full-time mathematics instructors and many part-time
mathematics instructors volunteer 1--4 hours per week in the SLC to help with
student demand. To help ensure usage throughout the SLC's operational hours,
instructors are notified by email of slow-traffic times; this allows the
instructors to direct students who need extra help to take advantage of those
times. Other communications such as announcements, ads, and newsletters are
sent out regularly.

Full-time faculty have constructed a `First week lecture series' that they
conduct on the first Friday of every term (except summer). It is designed to
review basic skills from MTH 20 through MTH 111. It is run in 50-minute
segments throughout the day with a 10-minute break between each segment. The
first offering of this series began in Winter 2012 with 100 students in
attendance; the attendance has since  grown steadily and  was up to
approximately 300 students by Fall 2013.

The Cascade SLC has formalized both the hiring process and the training process
for casual tutors. The department chairs interview potential tutors, determine
which levels they are qualified to tutor, and give guidance as to tutoring
strategies and rules. During their first term, each new tutor is always
scheduled in the learning center at the same time as a math instructor, and is
encouraged to seek math
and tutoring advice from that instructor.

\subsubsection{Rock Creek}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Rock Creek SLC has served about
690 math students with 3300 individual visits and 10 hours per student per term. (See \vref{app:tut:tab:SLC} for a full accounting.)

Everyone who works and learns in the Rock Creek SLC is looking forward to
moving into the newly-built space in Building 7 by Spring 2014. The new space
will bring the SLC closer to the library and into the same building as the WRC,
MC, and TLC.  Students seek tutoring largely in math and science, but
increasingly for accounting, computer basics, and also college reading.
Mathematics full-time faculty hold two of the required five office hours at the
tutoring center.

Motivated by the high levels of student demand for math tutoring, in 2012/13
the SLC piloted math tutoring by appointment two days per week. On each of the
two days a tutor leads thirty-minute individual sessions or one-hour group
tutoring sessions by appointment for most math levels.  After some tweaking of
days and times, we have settled on Tuesdays and Wednesdays.  Students who are
seeking a longer, more personalized or intensive tutoring session seem to
highly appreciate this new service.

Finally, the Rock Creek SLC has benefited over the last three years from collaboration
with advisors, counselors, librarians, the WRC, MC, and the Career Resource
Center in offering a wide variety of workshops as well as resource fairs to
support student learning.

\subsubsection{Southeast}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Southeast SLC has served about
280 math students with 1200 individual visits and 5 hours per student per term. (See \vref{app:tut:tab:SLC} for a full accounting.)

The SE SLC staff is looking forward to its move into the new tutoring center
facilities when the new buildings are completed. In the meantime, it has
expanded the math tutoring area by moving the writing tutoring to the back room
of the tutoring center.

Since the SE Tutoring Center opened in 2004, it has gone from serving an
average of 200 students per term (including math and other subjects) to serving
an average of 350 students per term in math alone.  With this increase in
students
seeking assistance, the staff has also grown; the SE SLC now has several faculty
members who work part time in the tutoring center.

Many SE math faculty members donate time to the tutoring center. We have
developed a service learning project where calculus students volunteer their
time in the tutoring center; this practice has been a great help to
students who utilize the tutoring center as well as a great opportunity for
calculus students to cement their own mathematical skills.

\subsubsection{Sylvania}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Sylvania SLC has served about
1100 math students with 6200 individual visits and 7 hours per student per
term. (See \vref{app:tut:tab:SLC} for a full accounting.)

The Sylvania SLC moved into a new location in Fall 2012; it is now in
the Library building, together with the Student Computing Center. The creation
of a learning commons is working out well and students are taking advantage of
having these different study resources in one place. Unfortunately, the new SLC
has less space available for math tutoring than the prior Student Success Center
which has been addressed by restructuring the space. Since enrollment remains high, having enough space
for all students seeking help remains a challenge.

PCC's incredible growth in enrollment created an attendant need for a dramatic
increase in the number of tutors available to students. This increased need has
been partially addressed by an increase in the budget set aside for paid tutors
as well as a heightened solicitation for volunteer tutors. Many
instructors (both full-time and part-time) have helped by volunteering in the
Sylvania SLC; for several years, the center was also able to recruit up to 10
work-study tutors per academic year, but with recent Federal changes to
Financial Aid, the Math Center is now only allowed two work-study tutors per
year; this restriction has led to a decrease of up to 50 tutoring hours per
week.

In addition to tutoring, the Sylvania SLC hosts the self-paced ALC math
classes, provides study material, and offers resources and workshops for
students to prepare for the Compass placement test. Efforts are also underway
to modernize a vast library of paper-based materials by putting them online and
making them available in alternate formats.


\section[Student services]{Provide information on how Advising, Counseling,
Disability Services and other student services impact students. }

Perhaps more than ever, the Math SAC appreciates and values the role of student
services in fostering success for our
students. In our development of an NSF-IUSE proposal (see
\vref{over:subsub:nsfiuse}), discussions and
planning returned again and again to student services such as advising,
placement testing, and counseling. As we look ahead hopefully toward a
realization of the structure that we envisioned, we will keep these services as
essential partners in serving our students. The current status of these
services follows.

\subsection{Advising and counseling}
The advising and counseling departments play a vital role in creating pathways
for student success; this is especially important when it comes to helping
students successfully navigate their mathematics courses.  Historically there
have been incidents of miscommunication between various math departments and
their campus counterparts in advising, but over the past few years a much more
deliberate effort to build strong communication links  between the two has
resulted in far fewer of these incidents.

The advising departments have been very responsive to requests made by the
mathematics departments and have been clear that there are
policies in place that prevent them from implementing some of the changes we
would like.

For example, in the past many advisers would make placement decisions based
upon criteria that the Math SAC felt weren't sufficient to support the
decision.   One example of this was placing students into classes based upon a
university's prerequisite structure rather than PCC's prerequisite structure.
When the advisers were made aware that this frequently led to students
enrolling in courses for which they were not prepared for success, the advising
department instituted an ironclad policy not to give any student permission to
register for a course unless there was documented evidence that the student had
passed a class that could be transcribed to PCC as the PCC prerequisite for
the course.  Any student who wants permission without a satisfied prerequisite
or adequate Compass score is now directed to a math faculty chair or to the
instructor of the specific section in which the student wishes to enroll.

On the downside, there are things we would like the advisers to do that we
have come to learn they cannot do.  For example, for several years the policy
of the Math SAC has been that prerequisites that were satisfied at other
colleges or universities would only be `automatically' accepted if they were
less than three years old.  Many instructors in the math department were under
the impression that this policy was in place in the advising department, but it
was discovered in 2012 that not only is this policy \emph{not} in place but the
policy in fact cannot be enforced by anyone
(including math faculty).   Apparently such a policy is enforceable only if
explicit prerequisite time-limits are written into the CCOGs.

The advising department had been aware of the prerequisite issue for six or
seven years, but somehow the word had not been passed along to the general math
faculty.  This serves as an example that both advising supervisors and the math
department chairs need to make every effort possible to inform all relevant
parties of policy changes in a clear and timely manner.  Towards that end, the
math department at Sylvania Campus has now been assigned an official liaison in
the Sylvania advising department. and we believe that similar connections
should be created on the other campuses as well.

With the college's new focus on student completion, the relationship between
the math departments and advising departments needs to become much stronger.
Initial placement plays a critical role in completion, as do other things such
as enrollment into necessary study skills classes and consecutive term-to-term
enrollment through a sequence of courses.  We need to make sure that the
advisers have all of the tools necessary to help students make the best choices
and the advisers need to help us understand their perspective on the needs of
students enrolling in mathematics courses.  To help establish this
collaborative environment, a Math SAC ad hoc committee has been formed to
investigate and address advising issues, placement issues, and study
skills issues;  the committee is going to ask several people involved in
advising and counseling to join the committee.  It has been speculated that
perhaps such a committee should not be under the direct purview of the Math
SAC; if the administration decides to create a similar committee under
someone else's direction we ask that any such committee have a large contingent
of math faculty.

\recommendation[PCC Cabinet, Deans of Students, Advising]{All four campuses should have an
    official advising liaison and the
    four liaisons should themselves have an established relationship.  Ideally we
    would like to have one adviser at each campus dedicated solely to math advising
issues.}

\recommendation[Math SAC, Advising, ROOTS]{ A committee consisting of advisers,
    math faculty, and other relevant parties
    (e.g.\ ROOTS representation) should be formed to investigate and establish
    policies related to student success in mathematics courses.  The issues to
    investigate include, but are not limited to,  placement, study skills, and
other college success skills as they relate to mathematics courses.}

\subsection{Testing centers}
At the time we wrote our last program review there were very uneven procedures
at the various testing centers which caused a lot of problems; the
inconsistencies were especially problematic for online instructors and their
students---see \cite{mathprogramreview2003}, page 26 .  We are pleased that the testing centers recognized that
inconsistency as a problem and they addressed the issue in a forthright way.
The testing centers now have uniform policies and they have made great strides
in making their services easily accessible to students and instructors alike.
For example, the ability to make testing arrangements online has been a
tremendous help as has the increase in the number of options by which a
completed exam can be returned to the instructor.

A limited number of hours of operation remains a problem at each of the testing
centers;   evening and weekend hours are not offered and testing times during
the remaining time are limited; for example, the Cascade Testing Center
offers only four start times for make up exams exam week.  It appears to us that the size of  the
facilities and the number of personnel  have not increased in equal parts with
the dramatic increase in enrollment.   It also appears that the testing centers
have not been given adequate funding to offer hours that accommodate students
who can only come to campus during the evening or on a weekend.

This lack of access can be especially problematic for students registered in
math courses.  The majority of the math courses at PCC are taught by part-time
faculty and these faculty members do not have the same flexibility in their
schedule as full-time faculty to proctor their own exams; as such they are
especially dependent on the testing centers for make-up testing. This
dependency is all the more problematic since many part-time faculty teach
evening or Saturday classes and many of the students in those classes find it
difficult to come to campus during `normal business hours.' Additionally, the
Sylvania math department simply does not have the space required to
administer make-up testing in the office, so 100\% of its faculty are dependent
upon the testing centers for make-up testing;   we realize this puts a strain
on the testing centers.

\recommendation[PCC Cabinet]{We recommend that the space and staffing in the
testing centers be increased.}

\recommendation[PCC Cabinet, Deans of Students, Testing Centers]{We recommend that make-up
    testing be available as late as 9:00 {\sc p.m.}\ at least two days per week,
and that make-up testing hours be available every Saturday.}

As discussed on \cpageref{other:page:disabilityservices,needs:page:disabilityservices},
the Math SAC has a very positive and productive relationship with disability
services.  For example, disability services was very responsive when some
instructors began to question accommodation requests that contradicted specific
evaluation criteria mandated in CCOGs (e.g.~testing certain material without
student access to a calculator).  Kaela Parks came to the SAC and assured us
that any such accommodation request is something an instructor need only
consider; i.e., those type of accommodation requests are not mandates on the
part of disability services.  The speed with which we received clarity about
this issue is indicative of the strong connection that has been forged between
the mathematics departments and disability services.

Beginning in the 2012/13 AY, all communication regarding student accommodations
(both general and testing-specific) has been done online.
Because of issues such as notifications being filtered to spam files, not all
accommodation requests were being read by faculty.  At the  mathematics faculty
department chairs' request, Kaela Parks created a spaces page that allow the
faculty chairs monitor which instructors have one or more students with
accommodation needs and highlights in red any instructor who has an outstanding
issue (such as pending exam) that needs immediate attention.  This resource has
greatly diminished the number of incidents where a student has an
accommodation need that is not addressed in a timely manner.

\section[Patterns of scheduling]{Describe current patterns of scheduling (such
 as modality, class size, duration, DC times, location, or other), address the
pedagogy of the program/discipline and the needs of students.}
%\section[Patterns of scheduling]{Describe current patterns of scheduling (such as such as modality, class size, duration, times, location, or other).  How do these relate to the pedagogy of the program/discipline and/or the needs of students?} %new version of the question, from Kendra
\label{facilities:sec:scheduling}
The math departments schedule classes that start as early as 7:00 {\sc a.m.}\ and
others that run as late as 9:50 {\sc p.m.}  About 80\% of our math classes are offered
in a two-day-a week format, meeting either Monday-Wednesday or
Tuesday-Thursday.  Some sections are offered in a three-day-a-week format and a
few in a four-day-a-week format; sections are offered in these formats to
accommodate students who find it helpful to be introduced to less content in
any one class session.

We also schedule classes that meet only once a week; some of those classes are
scheduled on  Saturdays.   While once-weekly meetings are not an ideal format for
teaching mathematics, having such sections creates options for students who
cannot attend college more than one day a week.

We offer several courses online, the enrollment in which has jumped
dramatically over the past five years (see \vref{fig:sec3:F2Fenrollments} and the discussion
surrounding it).  We also offer classes in both a web/TV hybrid and an online/on-campus hybrid format.

On-campus class sizes generally range from 20 to 35 students; that number is
typically dependent on the room that is assigned for the class (see \cpageref{needs:page:classsize} and
\vref{app:sec:classsize}).  This has led
to some inconsistencies among campuses as distribution of classroom capacities
is not consistent from one campus to the next.

Teaching online presents unique obstacles for faculty and students alike.
Faculty members, like students, have different methods of addressing these
obstacles.  The SAC has a recommended capacity limit of twenty-five for each
section on its DL course offerings.  This recommendation was based upon a
determination that twenty-five is a reasonable class size given the extra
duties associated with teaching online.  Because the attrition rates in online
courses can be higher than that in on-campus courses, many DL instructors ask
that their class capacity be set at, say, thirty to accommodate for first week
attrition.

In addition to increased class sizes that account for anticipated attrition,
some faculty members choose to allow additional students when their workload
allows for the attendant extra work.  In fact, during Winter 2014, only fifteen
out of a total of forty-one DL sections are limited to twenty-five students.
Of the remaining DL sections, seven are capped between twenty-five and thirty,
twelve are capped in the mid-to-low thirties, and seven are capped at greater
than forty-five.   Further information about scheduling patterns, broken down
by campus, can be found in \vref{sec:app:courseschedule}.

There is no specific pedagogical dictates in most of our courses.  Class
activities can range from lecture to class-discussion to group-work to
student-board-work. Some instructors provide their students with pre-printed
lecture notes and examples, others write notes on the board; some instructors
have their students work mostly on computer-based activities, and yet others
mostly work problems from the textbook. The frequency with which each
instructor uses each approach is almost entirely up to him/her.  Many
instructors have a required online homework component, while others do not.

This diversity of classroom experience has both positive and negative
consequences.  On the positive side, it provides an environment that has the
potential to address a wide-range of learning styles.  On the negative side, it
can lead to very inconsistent experiences for students as they work their way
through a sequence.  The inconsistency is probably most prevalent and,
unfortunately, most  problematic at the DE level of instruction.
As the Math SAC looks for ways to increase completion rates for students who
place into developmental mathematics courses, serious attention will be given
to plans that increase the consistency of classroom experience for students;
consistency that is built upon evidence-based best practices.
        """

        formatted = r"""
% arara: pdflatex: {files: [MathSACpr2014]}
% !arara: indent: {overwrite: yes}
\chapter{Facilities and Support}
\begin{flushright}
    \includegraphics[width=8cm]{xkcd-806-tech_support-punchline}\\
    \url{http://xkcd.com}
\end{flushright}
\section[Space, technology, and equipment]{
    Describe how classroom space, classroom technology, laboratory space and equipment impact student success.
}

Over the past few years, efforts by the college to create classrooms containing the same basic equipment has helped tremendously with consistency issues.
The nearly universal presence of classroom podiums with attendant Audio Visual (AV) devices is considerably useful.
For example, many instructors use computer-based calculator emulators when instructing their students on calculator use---this allows explicit keystroking examples to be demonstrated that were not possible before the podiums appeared; the document cameras found in most classrooms are also used by most mathematics instructors.
Having an instructor computer with internet access has been a great help as instructors have access to a wide variety of tools to engage students, as well as a source for quick answers when unusual questions arise.

Several classrooms on the Sylvania campus have Starboards or Smart Boards integrated with their AV systems.
Many mathematics instructors use these tools as their primary presentation vehicles; documents can be preloaded into the software and the screens allow instructors to write their work directly onto the document.
Among other things, this makes it easy to save the work into pdf files that can be accessed by students outside of class.
This equipment is not used as much on the other campuses, but there are instructors on other campuses that say they would use them if they were widely available on their campus.

A few instructors have begun creating lessons with LiveScribe technology.
The technology allows the instructor to make an audio/visual record of their lecture without a computer or third person recording device; instructors can post a `live copy' of their actual class lecture online.
The students do not simply see a static copy of the notes that were written; the students see the notes emerge as they were being written and they hear the words that were spoken while they were written.
The use of LiveScribe technology is strongly supported by Disability Services, and for that reason alone continued experimentation with its use is strongly encouraged.

Despite all of the improvements that have been made in classrooms over the past few years, there still are some serious issues.

Rooms are assigned randomly, which often leads to mathematics classes being scheduled in rooms that are not appropriate for a math class.
For example, scheduling a math class in a room with individual student desks creates a lot of problems; many instructors have students take notes, refer to their text, and use their calculator all at the same time and there simply is not enough room on the individual desktops to keep all of that material in place.
More significantly, this furniture is especially ill-suited for group work.
Not only does the movement of desks and sharing of work exacerbate the materials issue (materials frequently falling off the desks), students simply cannot share their work in the efficient way that work can be shared when they are gathered about tables.
It would be helpful if all non-computer-based math classes could be scheduled in rooms with tables.

Another problem relates to an inadequate number of computerized classrooms and insufficient space in many of the existing computerized classroom; both of these shortages have greatly increased due to Bond-related construction.
Several sections of MTH 243 and MTH 244 (statistics courses), which are normally taught in computerized classrooms, \emph{have} been scheduled in regular classrooms.
Many of the statistics courses that were scheduled in computerized classrooms have been scheduled in rooms that seat only 28, 24, or even 20 students.
When possible, we generally limit our class capacities at 34 or 35.
Needless to say, running multiple sections of classes in rooms well below those capacities creates many problems.
This is especially problematic for student success, as it hinders students' ability to register due to undersized classrooms.

Finally, the computerized classrooms could be configured in such a way that maximizes potential for meaningful student engagement and minimizes potential for students to get off course due to internet access.
We believe that all computerized classrooms need to come equipped with software that allows the instructor control of the student computers such as LanSchool Classroom Management Software.
The need for this technology is dire; it will reduce or eliminate students being off task when using computers, and it will allow another avenue to facilitate instruction as the instructor will be able to `see' any student computer and `interact' with any student computer.
It can also be used to solicit student feedback in an anonymous manner.
The gathering of anonymous feedback can frequently provide a better gauge of the general level of understanding than activities such as the traditional showing of hands.

\recommendation[Scheduling]{
    All mathematics classes should be scheduled in rooms that are either computerized (upon request) or have multi-person tables (as opposed to individual desks).
}

\recommendation[Scheduling, Deans of Instruction, PCC Cabinet]{
    All computerized classrooms should have at least 30, if not 34, individual work stations.
}

\recommendation[Multimedia Services, Deans of Instruction, PCC Cabinet]{
    An adequate number of classrooms on all campuses should be equipped with Smartboards so that all instructors who want access to the technology can teach every one of their classes in rooms equipped with the technology.
}

\recommendation[Multimedia Services, TSS]{
    The disk image for all computerized classrooms should include software that allows the podium computer direct access to each student computer.
}

\section[
    Library and other outside-the-classroom information resources
]{
    Describe how students are using the library or other outside-the-classroom information resources.
}
We researched this topic by conducting a stratified sampling method survey of 976 on-campus students and 291 online students; the participants were chosen in a random manner.
We gave scantron surveys to the on-campus students and used SurveyMonkey for the online students.
We found that students are generally knowledgeable about library resources and other outside-the-classroom resources.
The complete survey, together with its results, is given in
\vref{app:sec:resourcesurvey}; we have summarized our comments to some of the more interesting questions below.

\begin{enumerate}[label=Q\arabic*.,font=\bf]
    \item Not surprisingly, library resources and other campus-based resources are used more frequently by our on-campus students than by our online students.
    This could be due to less frequent visits to campus for online students and/or online students already having similar resources available to them via the internet.
    \item We found that nearly 70\% of instructors include resource information in their syllabi.
    This figure was consistent regardless of the level of the class (DE/transfer level) or the employment status of the instructor (full/part-time).

    We found that a majority of our instructors are using online resources to connect with students.
    Online communication between students and instructors is conducted across many platforms such as instructor websites, Desire2Learn, MyPCC, online graphing applications, and online homework platforms.

    We found that students are using external educational websites such as
    \href{https://www.khanacademy.org/}{Khan Academy},
    \href{http://patrickjmt.com/}{PatrickJMT},
    \href{http://www.purplemath.com/}{PurpleMath}, and
    \href{http://www.youtube.com/}{YouTube}.
    The data suggest online students use these services more than on-campus students.
    \item The use of online homework (such as WeBWorK, MyMathLab, MyStatLab, and ALEKS) has grown significantly over the past few years.
    However, the data suggests that significantly more full-time instructors than part-time instructors are directing their students towards these tools (as either a required or optional component of the course).
    Additionally, there is a general trend that online homework programs are being used more frequently in online classes than in on-campus classes.
    Both of these discrepancies may reflect the need to distribute more information to faculty about these software resources.
    \item The Math SAC needs to address whether or not we should be requiring students to use online resources that impose additional costs upon the students and, if so, what would constitute a reasonable cost to the student.
    To that end, our survey asked if students would be willing to pay up to \$35 to access online homework and other resources.
    We found that online students were more willing to pay an extra fee than those enrolled in on-campus classes.
    \setcounter{enumi}{6}
    \item The PCC mathematics website offers a wealth of materials that are frequently accessed by students.
    These include course-specific supplements, calculator manuals, and the required Calculus I lab manual; all of these materials were written by PCC mathematics faculty.
    Students may print these materials for free from any PCC computer lab.
    The website also links to PCC-specific information relevant to mathematics students (such as tutoring resources) as well as outside resources (such as the Texas Instruments website).
    \setcounter{enumi}{8}
    \item In addition to the previously mentioned resources we also encourage students to use resources offered at PCC such as on-campus Student Learning Centers, online tutoring, Collaborate, and/or Elluminate.
    A significant number of students registered in on-campus sections are using these resources whereas students enrolled in online sections generally are not.
    This is not especially surprising since on-campus students are, well, on campus whereas many online students rarely visit a campus.
\end{enumerate}

\recommendation[Math SAC]{
    The majority of our data suggests that students are using a variety of resources to further their knowledge.
    We recommend that instructors continue to educate students about both PCC resources and non-PCC resources.
    We need to uniformly encourage students to use resources such as online tutoring, Student Learning Centers, Collaborate, and/or Elluminate; this includes resource citations in each and every course syllabus.
}

\recommendation[Faculty Department Chairs]{
    A broader education campaign should be engaged to distribute information to part-time faculty regarding online homework such as WeBWorK, MyMathLab, MyStatLab, and ALEKS.
}

\recommendation[Math SAC]{
    Instructors should consider quality, accessibility and cost to students when requiring specific curriculum materials.
}

\section[Clerical, technical, administrative and/or tutoring support]{
    Provide information on clerical, technical, administrative and/or tutoring support.
}

The Math SAC has a sizable presence on each of PCC's three campuses and at Southeast Center (soon to be a campus in its own right).
Each campus houses a math department within a division of that campus.
The clerical, technical, administrative, and tutoring support systems are best described on location-by-location basis.

\subsection{Clerical, technical, and administrative support}

Across the district, our SAC has an excellent and very involved administrative liaison, Dr.
Alyson Lighthart.
We would like to thank her for her countless hours of support in attending our SAC meetings and being available to the SAC Co-Chairs.
She provides us with thoughtful feedback and insightful perspectives that help us gather our thoughts and make sound decisions.

\subsubsection{Cascade}
The Cascade math department belongs to the Math, Sciences, Health and PE division.
The math department is located on the third floor of the student services building, sharing a floor with the ROOTS office.
The math department also shares space with allied health support staff, medical professions faculty, medical assisting faculty and the Cascade academic intervention specialists (one of whom is also a math part-time faculty).
Part-time math faculty share 11 cubicles, each with a computer.
Our 7 full-time instructors are paired in offices that open up to the part-time cubicles.
We have space in our offices for another full time faculty member as we lost a temporary full-time position at the start of the 2013 academic year.
In Winter 2014, a collective 42 faculty share one high speed Ricoh printer and one copy machine.
Our division offices are located in another building.
We have a dedicated administrative assistant at the front desk who helps students and faculty most days from 8 {\sc a.m.--5 p.m.}

\subsubsection{Rock Creek}
The Rock Creek math department is located in the same floor as the division it belongs to (Mathematics, Aviation, and Industrial Technology) and it is shared with Computer Science.
Part-time faculty share fourteen cubicles, each with a computer, located in the same office as full-time instructors, that are used to prepare and meet with students.
The sixty-five plus faculty share two high speed printers that can collate, staple and allow double sided printing, and one high speed scanner.
Currently we have reached space capacity and we will have to re-think the current office configuration in order to add one more full-time faculty member next Fall.
Two years ago the Rock Creek math department added a dedicated administrative assistant, which has helped with scheduling needs, coordinating part-time faculty needs, and providing better service to the students.

\subsubsection{Southeast}
The clerical and administrative setup at Southeast has changed, as of Winter 2014.
There was a recent restructuring of divisions.
What used to be the Liberal Arts and Sciences Division split into two divisions: the Liberal Arts and CTE Division (which is in the first floor of Scott Hall, Room 103, where the Liberal Arts and Sciences used to be) and the Math and Science Division (which is on the \nth{2} floor of the new Student Commons Building, Room 214).
All of the math and science faculty are now in this new space, including the part-time instructors (everybody was scattered before, so this is a welcome change).

All of the department chairs have their own offices (with doors), while the rest of the faculty (full-time and part-time) occupy cubicle spaces (approximately 20 cubicles in the space, shared by 4--5 faculty per cubicle).
There are two administrative assistants, one of whom is with the math and science faculty and the other of whom is in charge of the STEM program.
There is also one clerical staff member.

There is one Ricoh printer in the space, along with a fax machine.
Any and all supplies (markers, erasers, etc.) are located across the hall in a designated staff room.

\subsubsection{Sylvania}
The Sylvania math department belongs to the Math and Industrial Technology division, which is located in the neighboring automotive building.
The math department is currently located in two separate areas of adjacent buildings as of Fall 2013, when the developmental math faculty officially merged with the math department.
This separation will soon be remedied by construction of the new math department area, scheduled to be completed during Spring 2014.
This new location will be next door to the Engineering department, and will share a conference room, copy machine room, and kitchen.
The math department will include two department chair offices, seventeen full-time instructor cubicles, six additional cubicles shared by part-time faculty, and two flex-space rooms.
Each of the cubicles will have a computer, and there will be two shared laser printers plus one color scanner in the department office.

Our two administrative assistants work an overlapped schedule, which provides dual coverage during the busy midday times and allows the office to remain open to students and visitors for eleven hours.
These assistants do an incredible job serving both student and faculty needs, including: scheduling assistance, interfacing with technical support regarding office and classroom equipment, maintaining supplies inventory, arranging for substitute instructors, securing signatures and processing department paperwork, guiding students to campus resources, and organizing syllabi and schedules from approximately 70 math instructors.

Our math department has frequent interaction with both Audio-Visual and Technology Solution Services.
Responses by AV to instructor needs in the classroom are extremely prompt--typically within minutes of the notification of a problem.
Since the math department is very technology-oriented, we have many needs that require the assistance of TSS.
Work orders for computer equipment and operational issues that arise on individual faculty computers can take quite a long time to be implemented or to be resolved.
This may be due to the sheer volume of requests that they are processing, but more information during the process, especially notes of any delays, would be welcomed.

\subsection{Tutoring support}
PCC has a Student Learning Center (SLC) on each campus.
It is a testament to PCC's commitment to student success that the four SLCs exist.
However, discrepancies such as unequal distribution of resources, inconsistency in the number and nature of tutors (including faculty `donating time' to the centers), and disparate hours of operation present challenges to students trying to navigate their way through different centers.

\recommendation[PCC Cabinet, Deans of Students, Deans of Instructions, Student Learning Centers]{
    The college should strive for more consistency with its Student Learning Centers.
    We feel that the centers would be an even greater resource if they were more consistent in structure, resource availability, physical space, and faculty support.
}

Over the last five years the general environment of PCC has been greatly impacted by historically-unmatched enrollment growth (see
\vref{fig:sec3:DLenrollments,fig:sec3:F2Fenrollments}).
PCC's four Student Learning Centers have been greatly affected by this (see \vref{app:sec:tutoringhours}).
Most notably, the number of students seeking math tutoring has increased dramatically.
Unfortunately, this increase in student need has not been met by increase in tutors or tutoring resources.
As a result the amount of attention an individual student receives has decreased in a substantive way, leaving students often frustrated and without the help they needed.
Consequently, the numbers of students dropped again as students stopped even trying.
While some of this growth has been (or will be) accommodated by increasing the physical space available for tutoring (i.e., by the construction of new facilities at Rock Creek and Southeast), that is still not enough since personnel resources were not increased at the same rate and work-study awards have been decreased significantly.
A comprehensive plan needs to be developed and implemented that will ensure each and every student receives high-quality tutoring in a consistent and consistently accessible manner.

As it now stands, the operation of the SLCs is completely campus driven.
As such, reporting on the current status needs to be done on a campus-by-campus basis.

\subsubsection{Cascade}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Cascade SLC has served about 680 math students with 3900 individual visits and 8 hours per student per term.
(See \vref{app:tut:tab:SLC} for a full accounting.)

The Cascade SLC has increased its operating hours in response to student demand.
Statistics tutoring is now offered at most times and the introduction of online homework has led to `Hybrid Tutoring', where students receive tutoring while working on their online homework.

At the Cascade Campus, all full-time mathematics instructors and many part-time mathematics instructors volunteer 1--4 hours per week in the SLC to help with student demand.
To help ensure usage throughout the SLC's operational hours, instructors are notified by email of slow-traffic times; this allows the instructors to direct students who need extra help to take advantage of those times.
Other communications such as announcements, ads, and newsletters are sent out regularly.

Full-time faculty have constructed a `First week lecture series' that they conduct on the first Friday of every term (except summer).
It is designed to review basic skills from MTH 20 through MTH 111.
It is run in 50-minute segments throughout the day with a 10-minute break between each segment.
The first offering of this series began in Winter 2012 with 100 students in attendance; the attendance has since grown steadily and was up to approximately 300 students by Fall 2013.

The Cascade SLC has formalized both the hiring process and the training process for casual tutors.
The department chairs interview potential tutors, determine which levels they are qualified to tutor, and give guidance as to tutoring strategies and rules.
During their first term, each new tutor is always scheduled in the learning center at the same time as a math instructor, and is encouraged to seek math and tutoring advice from that instructor.

\subsubsection{Rock Creek}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Rock Creek SLC has served about 690 math students with 3300 individual visits and 10 hours per student per term.
(See \vref{app:tut:tab:SLC} for a full accounting.)

Everyone who works and learns in the Rock Creek SLC is looking forward to moving into the newly-built space in Building 7 by Spring 2014.
The new space will bring the SLC closer to the library and into the same building as the WRC, MC, and TLC.
Students seek tutoring largely in math and science, but increasingly for accounting, computer basics, and also college reading.
Mathematics full-time faculty hold two of the required five office hours at the tutoring center.

Motivated by the high levels of student demand for math tutoring, in 2012/13 the SLC piloted math tutoring by appointment two days per week.
On each of the two days a tutor leads thirty-minute individual sessions or one-hour group tutoring sessions by appointment for most math levels.
After some tweaking of days and times, we have settled on Tuesdays and Wednesdays.
Students who are seeking a longer, more personalized or intensive tutoring session seem to highly appreciate this new service.

Finally, the Rock Creek SLC has benefited over the last three years from collaboration with advisors, counselors, librarians, the WRC, MC, and the Career Resource Center in offering a wide variety of workshops as well as resource fairs to support student learning.

\subsubsection{Southeast}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Southeast SLC has served about 280 math students with 1200 individual visits and 5 hours per student per term.
(See \vref{app:tut:tab:SLC} for a full accounting.)

The SE SLC staff is looking forward to its move into the new tutoring center facilities when the new buildings are completed.
In the meantime, it has expanded the math tutoring area by moving the writing tutoring to the back room of the tutoring center.

Since the SE Tutoring Center opened in 2004, it has gone from serving an average of 200 students per term (including math and other subjects) to serving an average of 350 students per term in math alone.
With this increase in students seeking assistance, the staff has also grown; the SE SLC now has several faculty members who work part time in the tutoring center.

Many SE math faculty members donate time to the tutoring center.
We have developed a service learning project where calculus students volunteer their time in the tutoring center; this practice has been a great help to students who utilize the tutoring center as well as a great opportunity for calculus students to cement their own mathematical skills.

\subsubsection{Sylvania}
Averaging over non-summer terms from Fall 2008 to Spring 2013, the Sylvania SLC has served about 1100 math students with 6200 individual visits and 7 hours per student per term.
(See \vref{app:tut:tab:SLC} for a full accounting.)

The Sylvania SLC moved into a new location in Fall 2012; it is now in the Library building, together with the Student Computing Center.
The creation of a learning commons is working out well and students are taking advantage of having these different study resources in one place.
Unfortunately, the new SLC has less space available for math tutoring than the prior Student Success Center which has been addressed by restructuring the space.
Since enrollment remains high, having enough space for all students seeking help remains a challenge.

PCC's incredible growth in enrollment created an attendant need for a dramatic increase in the number of tutors available to students.
This increased need has been partially addressed by an increase in the budget set aside for paid tutors as well as a heightened solicitation for volunteer tutors.
Many instructors (both full-time and part-time) have helped by volunteering in the Sylvania SLC; for several years, the center was also able to recruit up to 10 work-study tutors per academic year, but with recent Federal changes to Financial Aid, the Math Center is now only allowed two work-study tutors per year; this restriction has led to a decrease of up to 50 tutoring hours per week.

In addition to tutoring, the Sylvania SLC hosts the self-paced ALC math classes, provides study material, and offers resources and workshops for students to prepare for the Compass placement test.
Efforts are also underway to modernize a vast library of paper-based materials by putting them online and making them available in alternate formats.

\section[Student services]{
    Provide information on how Advising, Counseling, Disability Services and other student services impact students.
}

Perhaps more than ever, the Math SAC appreciates and values the role of student services in fostering success for our students.
In our development of an NSF-IUSE proposal (see
\vref{over:subsub:nsfiuse}), discussions and planning returned again and again to student services such as advising, placement testing, and counseling.
As we look ahead hopefully toward a realization of the structure that we envisioned, we will keep these services as essential partners in serving our students.
The current status of these services follows.

\subsection{Advising and counseling}
The advising and counseling departments play a vital role in creating pathways for student success; this is especially important when it comes to helping students successfully navigate their mathematics courses.
Historically there have been incidents of miscommunication between various math departments and their campus counterparts in advising, but over the past few years a much more deliberate effort to build strong communication links between the two has resulted in far fewer of these incidents.

The advising departments have been very responsive to requests made by the mathematics departments and have been clear that there are policies in place that prevent them from implementing some of the changes we would like.

For example, in the past many advisers would make placement decisions based upon criteria that the Math SAC felt weren't sufficient to support the decision.
One example of this was placing students into classes based upon a university's prerequisite structure rather than PCC's prerequisite structure.
When the advisers were made aware that this frequently led to students enrolling in courses for which they were not prepared for success, the advising department instituted an ironclad policy not to give any student permission to register for a course unless there was documented evidence that the student had passed a class that could be transcribed to PCC as the PCC prerequisite for the course.
Any student who wants permission without a satisfied prerequisite or adequate Compass score is now directed to a math faculty chair or to the instructor of the specific section in which the student wishes to enroll.

On the downside, there are things we would like the advisers to do that we have come to learn they cannot do.
For example, for several years the policy of the Math SAC has been that prerequisites that were satisfied at other colleges or universities would only be `automatically' accepted if they were less than three years old.
Many instructors in the math department were under the impression that this policy was in place in the advising department, but it was discovered in 2012 that not only is this policy \emph{not} in place but the policy in fact cannot be enforced by anyone (including math faculty).
Apparently such a policy is enforceable only if explicit prerequisite time-limits are written into the CCOGs.

The advising department had been aware of the prerequisite issue for six or seven years, but somehow the word had not been passed along to the general math faculty.
This serves as an example that both advising supervisors and the math department chairs need to make every effort possible to inform all relevant parties of policy changes in a clear and timely manner.
Towards that end, the math department at Sylvania Campus has now been assigned an official liaison in the Sylvania advising department.
and we believe that similar connections should be created on the other campuses as well.

With the college's new focus on student completion, the relationship between the math departments and advising departments needs to become much stronger.
Initial placement plays a critical role in completion, as do other things such as enrollment into necessary study skills classes and consecutive term-to-term enrollment through a sequence of courses.
We need to make sure that the advisers have all of the tools necessary to help students make the best choices and the advisers need to help us understand their perspective on the needs of students enrolling in mathematics courses.
To help establish this collaborative environment, a Math SAC ad hoc committee has been formed to investigate and address advising issues, placement issues, and study skills issues; the committee is going to ask several people involved in advising and counseling to join the committee.
It has been speculated that perhaps such a committee should not be under the direct purview of the Math SAC; if the administration decides to create a similar committee under someone else's direction we ask that any such committee have a large contingent of math faculty.

\recommendation[PCC Cabinet, Deans of Students, Advising]{
    All four campuses should have an official advising liaison and the four liaisons should themselves have an established relationship.
    Ideally we would like to have one adviser at each campus dedicated solely to math advising issues.
}

\recommendation[Math SAC, Advising, ROOTS]{
    A committee consisting of advisers, math faculty, and other relevant parties (e.g.\ ROOTS representation) should be formed to investigate and establish policies related to student success in mathematics courses.
    The issues to investigate include, but are not limited to, placement, study skills, and other college success skills as they relate to mathematics courses.
}

\subsection{Testing centers}
At the time we wrote our last program review there were very uneven procedures at the various testing centers which caused a lot of problems; the inconsistencies were especially problematic for online instructors and their students---see \cite{mathprogramreview2003}, page 26 .
We are pleased that the testing centers recognized that inconsistency as a problem and they addressed the issue in a forthright way.
The testing centers now have uniform policies and they have made great strides in making their services easily accessible to students and instructors alike.
For example, the ability to make testing arrangements online has been a tremendous help as has the increase in the number of options by which a completed exam can be returned to the instructor.

A limited number of hours of operation remains a problem at each of the testing centers; evening and weekend hours are not offered and testing times during the remaining time are limited; for example, the Cascade Testing Center offers only four start times for make up exams exam week.
It appears to us that the size of the facilities and the number of personnel have not increased in equal parts with the dramatic increase in enrollment.
It also appears that the testing centers have not been given adequate funding to offer hours that accommodate students who can only come to campus during the evening or on a weekend.

This lack of access can be especially problematic for students registered in math courses.
The majority of the math courses at PCC are taught by part-time faculty and these faculty members do not have the same flexibility in their schedule as full-time faculty to proctor their own exams; as such they are especially dependent on the testing centers for make-up testing.
This dependency is all the more problematic since many part-time faculty teach evening or Saturday classes and many of the students in those classes find it difficult to come to campus during `normal business hours.' Additionally, the Sylvania math department simply does not have the space required to administer make-up testing in the office, so 100\% of its faculty are dependent upon the testing centers for make-up testing; we realize this puts a strain on the testing centers.

\recommendation[PCC Cabinet]{
    We recommend that the space and staffing in the testing centers be increased.
}

\recommendation[PCC Cabinet, Deans of Students, Testing Centers]{
    We recommend that make-up testing be available as late as 9:00 {\sc p.m.}\ at least two days per week, and that make-up testing hours be available every Saturday.
}

As discussed on \cpageref{other:page:disabilityservices,needs:page:disabilityservices}, the Math SAC has a very positive and productive relationship with disability services.
For example, disability services was very responsive when some instructors began to question accommodation requests that contradicted specific evaluation criteria mandated in CCOGs (e.g.~testing certain material without student access to a calculator).
Kaela Parks came to the SAC and assured us that any such accommodation request is something an instructor need only consider; i.e., those type of accommodation requests are not mandates on the part of disability services.
The speed with which we received clarity about this issue is indicative of the strong connection that has been forged between the mathematics departments and disability services.

Beginning in the 2012/13 AY, all communication regarding student accommodations (both general and testing-specific) has been done online.
Because of issues such as notifications being filtered to spam files, not all accommodation requests were being read by faculty.
At the mathematics faculty department chairs' request, Kaela Parks created a spaces page that allow the faculty chairs monitor which instructors have one or more students with accommodation needs and highlights in red any instructor who has an outstanding issue (such as pending exam) that needs immediate attention.
This resource has greatly diminished the number of incidents where a student has an accommodation need that is not addressed in a timely manner.

\section[Patterns of scheduling]{
    Describe current patterns of scheduling (such as modality, class size, duration, DC times, location, or other), address the pedagogy of the program/discipline and the needs of students.
}
%\section[Patterns of scheduling]{Describe current patterns of scheduling (such as such as modality, class size, duration, times, location, or other).  How do these relate to the pedagogy of the program/discipline and/or the needs of students?} %new version of the question, from Kendra
\label{facilities:sec:scheduling}
The math departments schedule classes that start as early as 7:00 {\sc a.m.}\ and others that run as late as 9:50 {\sc p.m.} About 80\% of our math classes are offered in a two-day-a week format, meeting either Monday-Wednesday or Tuesday-Thursday.
Some sections are offered in a three-day-a-week format and a few in a four-day-a-week format; sections are offered in these formats to accommodate students who find it helpful to be introduced to less content in any one class session.

We also schedule classes that meet only once a week; some of those classes are scheduled on Saturdays.
While once-weekly meetings are not an ideal format for teaching mathematics, having such sections creates options for students who cannot attend college more than one day a week.

We offer several courses online, the enrollment in which has jumped dramatically over the past five years (see \vref{fig:sec3:F2Fenrollments} and the discussion surrounding it).
We also offer classes in both a web/TV hybrid and an online/on-campus hybrid format.

On-campus class sizes generally range from 20 to 35 students; that number is typically dependent on the room that is assigned for the class (see \cpageref{needs:page:classsize} and
\vref{app:sec:classsize}).
This has led to some inconsistencies among campuses as distribution of classroom capacities is not consistent from one campus to the next.

Teaching online presents unique obstacles for faculty and students alike.
Faculty members, like students, have different methods of addressing these obstacles.
The SAC has a recommended capacity limit of twenty-five for each section on its DL course offerings.
This recommendation was based upon a determination that twenty-five is a reasonable class size given the extra duties associated with teaching online.
Because the attrition rates in online courses can be higher than that in on-campus courses, many DL instructors ask that their class capacity be set at, say, thirty to accommodate for first week attrition.

In addition to increased class sizes that account for anticipated attrition, some faculty members choose to allow additional students when their workload allows for the attendant extra work.
In fact, during Winter 2014, only fifteen out of a total of forty-one DL sections are limited to twenty-five students.
Of the remaining DL sections, seven are capped between twenty-five and thirty, twelve are capped in the mid-to-low thirties, and seven are capped at greater than forty-five.
Further information about scheduling patterns, broken down by campus, can be found in \vref{sec:app:courseschedule}.

There is no specific pedagogical dictates in most of our courses.
Class activities can range from lecture to class-discussion to group-work to student-board-work.
Some instructors provide their students with pre-printed lecture notes and examples, others write notes on the board; some instructors have their students work mostly on computer-based activities, and yet others mostly work problems from the textbook.
The frequency with which each instructor uses each approach is almost entirely up to him/her.
Many instructors have a required online homework component, while others do not.

This diversity of classroom experience has both positive and negative consequences.
On the positive side, it provides an environment that has the potential to address a wide-range of learning styles.
On the negative side, it can lead to very inconsistent experiences for students as they work their way through a sequence.
The inconsistency is probably most prevalent and, unfortunately, most problematic at the DE level of instruction.
As the Math SAC looks for ways to increase completion rates for students who place into developmental mathematics courses, serious attention will be given to plans that increase the consistency of classroom experience for students; consistency that is built upon evidence-based best practices.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_pcc_program_review2(self):
        text = r"""
% arara: pdflatex: {files: [MathSACpr2014]}
% !arara: indent: {overwrite: yes}
\chapter[Faculty composition and qualifications]{Faculty:  reflect on the
composition, qualifications and development of the faculty}
\epigraph{ %
    I want to tell you what went through my head as I saw the D on my \nth{3} exam in
    Calc II:  ``f\#\$king a\&\$hole!''  That D changed my life.  The feeling of
    failure, not from my incompetence but rather my laziness.
    I want to let you know that every single success in my life now is due in part
    to your teachings.  I can't thank you enough \& I hope that if for nothing
    else, you have made a great influence on me.}{PCC Mathematics
Student, December 2013}

\section[Faculty composition]{Provide information on each of the following:}
\subsection[Quantity and quality of the faculty]{Quantity and quality of the faculty needed to meet the needs of the
program or discipline.}
The total number of full-time faculty at all campuses between 2011 and 2013
varied between 36 to 41 and the
part-time faculty varied between 143 to 158 on any given term,  not including
Summer.     The percent of \emph{all} courses (pre-college and college level)
taught by full-time instructors during this time period varied from a low of
22\% at Rock Creek to a high of 29\% at Sylvania (see
\cref{app:tab:analysisPTFT}).

From the academic year 2008/09 to 2012/13 there was a significant increase in the
number of students taking math courses at all campuses as shown
\cref{reflect:tab:enrollment}.
\begin{table}[!htb]
    \centering
    \caption{Enrollment Difference from AY 08/09 to AY 12/13}
    \label{reflect:tab:enrollment}
    \begin{tabular}{lrr}
        \toprule
        Campus & Enrollment Difference & \% increase \\
        \midrule
        SY     & 5277                  & 48.59\%     \\
        CA     & 3666                  & 64.82\%     \\
        RC     & 5333                  & 55.87\%     \\
        ELC    & 3171                  & 103.09\%    \\
        \bottomrule
    \end{tabular}
\end{table}

\Cref{app:tab:analysisPTFT} summarizes the breakdown of courses taught by
full-time and part-time faculty from Summer 2011--Spring 2013; breakdowns
by \emph{term} are given in \vref{app:sec:analysisPTFT}.

\begin{table}[!htb]
    \centering
    \caption{Summary of sections taught (by campus) from Summer 2011--Spring 2013}
    \label{app:tab:analysisPTFT}
    % summary
    % summary
    % summary
    \pgfplotstableread[col sep=comma]{./data/sectionsTaughtPTFT/sectionsTaughtPTFT2011-2013.csv}\sectionsTaughtSummary
    \pgfplotstabletypeset[sectionFTPT]{\sectionsTaughtSummary}
\end{table}


In reference to ``quality of the faculty needed to meet the needs of the
discipline,''  it is insufficient to look at degree or experience
qualifications alone.  Even a short list of what we expect from our mathematics
faculty would include, but not be limited to that she/he:
\begin{itemize}
    \item possess an understanding of effective mathematics teaching
    methodologies and      strategies, and be able to adjust in response to
    student needs;
    \item  teach  the course content as outlined in CCOGs and with the appropriate mathematical  rigor;
    \item show genuine commitment to students' success;
    \item identify problems when students encounter difficulties learning;
    \item demonstrate an ongoing intellectual curiosity about the relationship
    between teaching and learning;
    \item manage classroom learning environments and effectively handle student
    discipline problems;
    \item demonstrate technological literacy needed in the teaching of mathematics;
    \item participate in professional organizations;
    \item develop, evaluate and revise the mathematics curricula;
    \item serve and contribute to the PCC community as a whole through campus and
    district wide committees and activities.
\end{itemize}
In addition, with the enormous enrollment increases of the past several years,
there are more students than ever needing both remediation in mathematics and
guidance in general about what it takes to be a successful college student.

Addressing this section heading directly, the `quantity' of full-time faculty
needed to achieve the `quality' goals noted above is currently inadequate.  It
is primarily the full-time faculty that has the time, resources and
institutional support to fully realize the expectations noted above.  Part-time
faculty are dedicated, but the expectations are different given the
many of the challenges they face (discussed below).   To increase the probability that a student moves successfully
through our mathematics courses without sacrificing quality, having a larger
full-time faculty presence than currently exists is needed.

In recognizing the need for more full-time faculty, we do not want to downplay
the skills and talents of our part-time faculty.  We have approximately 150
part-time instructors that serve our students each term, many of whom have
teaching experience from other colleges and universities; they bring additional
experiences from industry, other sciences, high school and middle school
education, and so much more.  Since they teach such a high percentage of our
classes, their success is crucial to our students' success.

Given the importance of part-time faculty, efforts needs to be made to minimize
the many challenges that are unique to them.  Many of these challenges are
created by the fact that part-timers frequently work on more than one campus or
have a second (or third) job beyond their work for PCC.  Many of the problems
are created by the institution itself.  The challenges include limited office
space, limited access to office computers and other resources, limited
opportunities to attend meetings, limited opportunities to engage in
professional development activities, limited opportunities for peer-to-peer
discourse.

\recommendation[Office of Academic and Student Affairs]{The college should
    continue to add new full-time math positions so that at each campus full-timers
    at least 40\% of all sections at both the DE and transfer level.}

\recommendation[Math SAC, PCC Cabinet, ACCEPT, PCCFFAP]{Given the heavy
    reliance on part-time faculty for staffing our courses, there is little chance
    that we can institutionalize significant changes in our DE courses without an
    empowered part-time work force. As such, we recommend that the college take
    action to support professional development for part-time faculty, provide
    adequate office space and tools for part-time faculty, and any recommendations
put forth by ACCEPT.}

\recommendation[PCC Cabinet, Human Resources]{The college should allow mathematics
    departments, at the discretion of each campus's faculty, to hire full-time
    faculty who meet the approved instructor qualifications for teaching at the
    pre-100 level but not the approved instructor qualifications for teaching at
    the post-100 level.  A large majority of our courses are at the DE level, and
    the needs of students enrolled in those courses are frequently different than
    the needs of students enrolled in undergraduate level courses.  Having a robust
    assortment of full-time faculty educational experience can only help in our
pursuit of increased student success and completion.}


\subsection[Faculty turnover]{Extent of faculty turnover and changes anticipated in the next five
years.}
Since 2011, ten full-time instructors have been hired and seven full-time
instructors have left campuses across the district (this includes full-time
temporary positions).  Of the seven full-time
instructors who left, five retired, one left to pursue other job opportunities,
and one returned to another teaching job after her temporary full-time position
terminated.  Three of the retirements occurred at Sylvania and one each at Rock
Creek and Cascade.  In addition to those that left the college, four full-time
instructors transferred from one campus to another.   Given no unexpected
events, we anticipate that these demographics will roughly be repeated over the
next five years.


Since 2011, 53 part-time instructors have been hired and 35 part-time
instructors have left campuses across the district.  Of the three campuses,
Rock Creek has the most part-time faculty turnover, followed by Cascade and
Sylvania.  Reasons for leaving varied, but at least eight of the part-time
instructors who left campuses simply moved to another campus in the district
(see \vref{app:sec:facultyDegrees}).

\subsection[Part-time faculty]{Extent of the reliance upon part-time faculty and how they compare
with full-time faculty in terms of educational and experiential backgrounds.}
Across the district, the mathematics departments rely heavily upon part-time
faculty to teach the majority of the math classes offered.  Between 2011 and
2013, 75.1\% of the classes at Cascade were taught by part-time instructors,
71.8\% at Rock Creek, 72.7\% at Southeast, and 59\% at Sylvania.  This reliance
on part-time faculty to teach classes has been a challenge to the departments
in a number of ways:
\begin{itemize}
    \item the turnover of part-time faculty is higher and
    thus there is a need to orient new employees more frequently and provide
    mentoring and guidance to them as well;
    \item many part-time faculty are on
    campus only to teach their courses, and thus often do not attend meetings and
    keep up with current SAC discussions on curriculum.
\end{itemize}
For these reasons, classes have a higher probability to be taught with less consistency than the
mathematics SAC would like.  Increasing the number of full-time faculty (and
thus decreasing the dependence on part-time faculty) would mitigate much of
this inconsistency; complete details are given in  \vref{app:sec:analysisPTFT}.

Part-time faculty educational backgrounds vary much more than the full-time
faculty backgrounds.  Full-time instructors have master's or doctorate degrees
in mathematics or related fields with extensive math graduate credits.  About a
quarter of the part-time instructors have bachelor's degrees and the rest have
either a master's or doctorate degree.  The part-time instructors come from a
variety of employment backgrounds and have different reasons for working
part-time.  They may be high school instructors (active or retired), may come
from a household in which only one member is working full time while the other
teaches part time, may be recently graduated MS or MAT students seeking full
time employment, may be working full time elsewhere in a non-educational field,
or may be retired from a non-educational field (see
\vref{app:sec:facultyDegrees}).
%  Is it true that a quarter of our PT faculty only have BS degrees?  How did
%  this happen?  I don't see room for that in the IQs.  How did you get this
%  data?

\subsection[Faculty diversity]{How the faculty composition reflects the diversity and cultural
competency goals of the institution.}
The mathematics SAC is deeply committed to fostering an inclusive campus
climate at each location that respects all individuals regardless of race,
color, religion, ethnicity, use of native language, national origin, sex,
marital status, height/weight ratio, disability, veteran status, age, or sexual
orientation.  Many of these human characteristics noted above are not
measurable nor necessarily discernible.  However, PCC does gather data on
gender and race/ethnicity, as detailed in \cref{reflect:tab:racialethnicmakeup}
(see also the extensive demographic data displayed in
\vref{app:sec:demographicdata}).

\begin{table}[!htb]
    \centering
    \caption{Racial/Ethnic Make-up of PCC Faculty and Students}
    \label{reflect:tab:racialethnicmakeup}
    \begin{tabular}{rrrr}
        \toprule
                                  & PT Faculty & FT Faculty & Students \\
        \midrule
        Male                      & 54.1\%     & 53.2\%     & 55\%     \\
        Female                    & 45.9\%     & 47\%       & 45\%     \\
        Asian /Pacific Islander   & 7.7\%      & 6.4\%      & 8\%      \\
        Black or African American & 1.1\%      & 0.0\%      & 6\%      \\
        Hispanic/Latino           & 2.2\%      & 4.3\%      & 11\%     \\
        Multiracial               & 1.1\%      & 0.0\%      & 3\%      \\
        Native American           & 0.0\%      & 0.0\%      & 1\%      \\
        Unknown/International     & 12.2\%     & 4.3\%      & 3\%      \\
        Caucasian                 & 75.7\%     & 85.1\%     & 68\%     \\
        \bottomrule
    \end{tabular}
\end{table}

Our SAC will continue to strive toward keeping our faculty body ethnically
diverse and culturally competent, but it is an area where improvement is
needed. In terms of hiring, there is a shortage of minorities in the Science, Technology, Engineering
and Mathematics (STEM) undergraduate and graduate programs, which makes our
recruitment of minority faculty difficult. \label{reflect:page:stem}

\recommendation[Math SAC, Division Deans]{Math chairs and deans should
    strongly recommend that full- and part-time faculty
attend workshops related to diversity and cultural competency issues.}

\recommendation[PCCFFAP, Division Deans]{Part-time faculty should be allowed
    to attend diversity/cultural awareness workshops in lieu of contractually
mandated quarterly meetings.}

\recommendation[Math SAC, Division Deans, Human Resources]{Hiring committees need to work with HR to identify
    and aggressively target mathematics graduate programs in the Northwest with
minority students who are seeking teaching positions in community colleges.}

\recommendation[Division Deans, Faculty Department Chairs]{Departments on all campuses should increase efforts to find candidates
    for the Faculty Diversity Internship Program \cite{affirmativeaction}.}

\section[Changes to instructor qualifications]{Report any changes the SAC has
 made to instructor qualifications since
the last review and the reason for the changes.}
In Spring 2011, prompted by the transfer of MTH 20 from Developmental
Education (DE) to the Mathematics SAC, the math instructor qualifications were
changed.  MTH 20 had been the only remaining mathematics course in the DE SAC.

The transfer included transitioning three full-time DE math instructors at
Sylvania into the Math Department at Sylvania.  At this time, instructor
qualifications for math faculty were examined and changed to reflect the
inclusion of DE math faculty.  It was determined that separate qualifications
should be written for pre-college and college level courses.  These
qualifications were written so that all of the full-time DE math faculty
transitioning into the math department (as well as any new DE math faculty
hired) were qualified to teach the pre-college level courses and any new math
faculty were qualified to teach all of the math courses.

For instance, a masters degree in mathematics education (instead of just
mathematics) was included as an optional qualification for full-time
instructors teaching pre-college level courses.  Also a masters degree in
mathematics education became an option for part-time instructors teaching MTH
211--213 (the sequence for elementary education math teachers).  Additionally,
at the request of the administration, the terms `part-time' and `full-time'
were removed from instructor qualifications in order to satisfy accreditation
requirements.  Instead of labeling what had traditionally been part-time
qualifications as `part-time,' these qualifications were labeled `Criteria for
Provisional Instructors.'

In Winter 2013, the math instructor qualifications were again changed at the
request of the math department chairs.  The `provisional' labeling
from the last revision had required math department chairs to regularly
re-certify part-time (`provisional') instructors.  In order to avoid this
unnecessary paperwork, the SAC adopted a three-tiered qualification structure
based on full-time, part-time, and provisionally-approved part-time instructors
(mainly graduate students currently working on graduate degrees).  The
part-time (non-provisional) tier was labeled `Demonstrated Competency.'
Complete details of instructor qualifications are given in \vref{app:sec:instructorquals}.


\section[Professional development activities]{How have professional development
 activities of the faculty contributed to the strength of the
 program/discipline? If such activities have resulted in instructional or
curricular changes, please describe.}

The members of the mathematics SAC, full-time and part-time alike, are very
committed to professional development.  As with members of any academic
discipline, the faculty in the Math SAC pursue professional development in a
variety of manners.  Traditionally these activities have been categorized in
ways such as `membership in professional organizations' or `presentations at
conferences'.  The members of the Math SAC do not in any way devalue the
engagement in such organizations or activities, and in fact a summative list of
such things can be found in \vref{app:sec:memberships}.

Nor do the members in any way diminish individual pursuit of professional
development.  In an attempt to acknowledge such pursuits, each member of the
full-time faculty was asked to submit one or two highlights of their
professional development activities over the past five years.  Those
submissions can be found in \vref{app:sec:professionaldevelop}.

It should be noted that the list of organizations and activities found in these
appendices are not exhaustive; they are merely a representative sample of
the types of professional development pursuits engaged in by members of the
Math SAC.

The members of the Math SAC realize that if there is going to be
institutional-level change that results in increased success and completion
rates for students enrolled in DE mathematics courses, there are going to have
to be targeted and on-going professional development activities with that goal
in mind and that all mathematics faculty, full-time and part-time, are going to
have to take advantage of those opportunities.  This is especially important
since many of our faculty members are not specialists in working with
developmental mathematics students. We look forward to working with the broader
PCC community as we pursue our common goal of increased student success and
completion, and we look forward to the college's support in providing
professional development opportunities that promote attainment of this goal.

\recommendation[PCC Cabinet]{The college should provide funds and other necessary resources
    that allow the SAC members to engage in targeted, on-going professional
    development geared toward realization of district-wide goals.  This should
    include, for example, support for activities such as annual two-day workshops
    focusing on goals such as universal adoption of evidence-based best
practices.}

\recommendation[Division Deans, Faculty Department Chairs, PCCFFAP, Completion Investment Council]{Each math department should create structures and policies that
    promote sustained professional development.  Institutionalization of practices
    such as faculty-inquiry-groups and peer-to-peer classroom visitations are
necessary components of sustained professional development.}

\recommendation[Math SAC, PCC Cabinet]{The college should continue to provide funds for activities
    such as conference attendance, professional organization membership, etc. At
    the same time, procedures should be put into place that allow for maximal
    dissemination of ``good ideas'' and maximum probability that said ideas grow into
sustained practices.}

\recommendation[Division Deans, Faculty Department Chairs, PCCFFAP]{Formalized procedures for mentoring new faculty, full-time and
    part-time alike, should be adopted and strictly observed.  Beginning a new job
    is a unique opportunity for rapid professional development, and we need to make
    sure that we provide as supportive and directed an opportunity for new faculty
    as possible so that the development happens in a positive and long-lasting
way.}
        """

        formatted = r"""
% arara: pdflatex: {files: [MathSACpr2014]}
% !arara: indent: {overwrite: yes}
\chapter[Faculty composition and qualifications]{
    Faculty: reflect on the composition, qualifications and development of the faculty
}
\epigraph{ %
    I want to tell you what went through my head as I saw the D on my \nth{3} exam in Calc II: ``f\#\$king a\&\$hole!'' That D changed my life.
    The feeling of failure, not from my incompetence but rather my laziness.
    I want to let you know that every single success in my life now is due in part to your teachings.
    I can't thank you enough \& I hope that if for nothing else, you have made a great influence on me.
}{
    PCC Mathematics Student, December 2013
}

\section[Faculty composition]{Provide information on each of the following:}
\subsection[Quantity and quality of the faculty]{
    Quantity and quality of the faculty needed to meet the needs of the program or discipline.
}
The total number of full-time faculty at all campuses between 2011 and 2013 varied between 36 to 41 and the part-time faculty varied between 143 to 158 on any given term, not including Summer.
The percent of \emph{all} courses (pre-college and college level) taught by full-time instructors during this time period varied from a low of 22\% at Rock Creek to a high of 29\% at Sylvania (see
\cref{app:tab:analysisPTFT}).

From the academic year 2008/09 to 2012/13 there was a significant increase in the number of students taking math courses at all campuses as shown
\cref{reflect:tab:enrollment}.
\begin{table}[!htb]
    \centering
    \caption{Enrollment Difference from AY 08/09 to AY 12/13}
    \label{reflect:tab:enrollment}
    \begin{tabular}{lrr}
        \toprule
        Campus & Enrollment Difference & \% increase \\
        \midrule
        SY     & 5277                  & 48.59\%     \\
        CA     & 3666                  & 64.82\%     \\
        RC     & 5333                  & 55.87\%     \\
        ELC    & 3171                  & 103.09\%    \\
        \bottomrule
    \end{tabular}
\end{table}

\Cref{app:tab:analysisPTFT} summarizes the breakdown of courses taught by full-time and part-time faculty from Summer 2011--Spring 2013; breakdowns by \emph{term} are given in \vref{app:sec:analysisPTFT}.

\begin{table}[!htb]
    \centering
    \caption{Summary of sections taught (by campus) from Summer 2011--Spring 2013}
    \label{app:tab:analysisPTFT}
    % summary
    % summary
    % summary
    \pgfplotstableread[col sep=comma]{./data/sectionsTaughtPTFT/sectionsTaughtPTFT2011-2013.csv}\sectionsTaughtSummary
    \pgfplotstabletypeset[sectionFTPT]{\sectionsTaughtSummary}
\end{table}

In reference to ``quality of the faculty needed to meet the needs of the discipline,'' it is insufficient to look at degree or experience qualifications alone.
Even a short list of what we expect from our mathematics faculty would include, but not be limited to that she/he:
\begin{itemize}
    \item possess an understanding of effective mathematics teaching methodologies and strategies, and be able to adjust in response to student needs;
    \item teach the course content as outlined in CCOGs and with the appropriate mathematical rigor;
    \item show genuine commitment to students' success;
    \item identify problems when students encounter difficulties learning;
    \item demonstrate an ongoing intellectual curiosity about the relationship between teaching and learning;
    \item manage classroom learning environments and effectively handle student discipline problems;
    \item demonstrate technological literacy needed in the teaching of mathematics;
    \item participate in professional organizations;
    \item develop, evaluate and revise the mathematics curricula;
    \item serve and contribute to the PCC community as a whole through campus and district wide committees and activities.
\end{itemize}
In addition, with the enormous enrollment increases of the past several years, there are more students than ever needing both remediation in mathematics and guidance in general about what it takes to be a successful college student.

Addressing this section heading directly, the `quantity' of full-time faculty needed to achieve the `quality' goals noted above is currently inadequate.
It is primarily the full-time faculty that has the time, resources and institutional support to fully realize the expectations noted above.
Part-time faculty are dedicated, but the expectations are different given the many of the challenges they face (discussed below).
To increase the probability that a student moves successfully through our mathematics courses without sacrificing quality, having a larger full-time faculty presence than currently exists is needed.

In recognizing the need for more full-time faculty, we do not want to downplay the skills and talents of our part-time faculty.
We have approximately 150 part-time instructors that serve our students each term, many of whom have teaching experience from other colleges and universities; they bring additional experiences from industry, other sciences, high school and middle school education, and so much more.
Since they teach such a high percentage of our classes, their success is crucial to our students' success.

Given the importance of part-time faculty, efforts needs to be made to minimize the many challenges that are unique to them.
Many of these challenges are created by the fact that part-timers frequently work on more than one campus or have a second (or third) job beyond their work for PCC.
Many of the problems are created by the institution itself.
The challenges include limited office space, limited access to office computers and other resources, limited opportunities to attend meetings, limited opportunities to engage in professional development activities, limited opportunities for peer-to-peer discourse.

\recommendation[Office of Academic and Student Affairs]{
    The college should continue to add new full-time math positions so that at each campus full-timers at least 40\% of all sections at both the DE and transfer level.
}

\recommendation[Math SAC, PCC Cabinet, ACCEPT, PCCFFAP]{
    Given the heavy reliance on part-time faculty for staffing our courses, there is little chance that we can institutionalize significant changes in our DE courses without an empowered part-time work force.
    As such, we recommend that the college take action to support professional development for part-time faculty, provide adequate office space and tools for part-time faculty, and any recommendations put forth by ACCEPT.
}

\recommendation[PCC Cabinet, Human Resources]{
    The college should allow mathematics departments, at the discretion of each campus's faculty, to hire full-time faculty who meet the approved instructor qualifications for teaching at the pre-100 level but not the approved instructor qualifications for teaching at the post-100 level.
    A large majority of our courses are at the DE level, and the needs of students enrolled in those courses are frequently different than the needs of students enrolled in undergraduate level courses.
    Having a robust assortment of full-time faculty educational experience can only help in our pursuit of increased student success and completion.
}

\subsection[Faculty turnover]{
    Extent of faculty turnover and changes anticipated in the next five years.
}
Since 2011, ten full-time instructors have been hired and seven full-time instructors have left campuses across the district (this includes full-time temporary positions).
Of the seven full-time instructors who left, five retired, one left to pursue other job opportunities, and one returned to another teaching job after her temporary full-time position terminated.
Three of the retirements occurred at Sylvania and one each at Rock Creek and Cascade.
In addition to those that left the college, four full-time instructors transferred from one campus to another.
Given no unexpected events, we anticipate that these demographics will roughly be repeated over the next five years.

Since 2011, 53 part-time instructors have been hired and 35 part-time instructors have left campuses across the district.
Of the three campuses, Rock Creek has the most part-time faculty turnover, followed by Cascade and Sylvania.
Reasons for leaving varied, but at least eight of the part-time instructors who left campuses simply moved to another campus in the district (see \vref{app:sec:facultyDegrees}).

\subsection[Part-time faculty]{
    Extent of the reliance upon part-time faculty and how they compare with full-time faculty in terms of educational and experiential backgrounds.
}
Across the district, the mathematics departments rely heavily upon part-time faculty to teach the majority of the math classes offered.
Between 2011 and 2013, 75.1\% of the classes at Cascade were taught by part-time instructors, 71.8\% at Rock Creek, 72.7\% at Southeast, and 59\% at Sylvania.
This reliance on part-time faculty to teach classes has been a challenge to the departments in a number of ways:
\begin{itemize}
    \item the turnover of part-time faculty is higher and thus there is a need to orient new employees more frequently and provide mentoring and guidance to them as well;
    \item many part-time faculty are on campus only to teach their courses, and thus often do not attend meetings and keep up with current SAC discussions on curriculum.
\end{itemize}
For these reasons, classes have a higher probability to be taught with less consistency than the mathematics SAC would like.
Increasing the number of full-time faculty (and thus decreasing the dependence on part-time faculty) would mitigate much of this inconsistency; complete details are given in \vref{app:sec:analysisPTFT}.

Part-time faculty educational backgrounds vary much more than the full-time faculty backgrounds.
Full-time instructors have master's or doctorate degrees in mathematics or related fields with extensive math graduate credits.
About a quarter of the part-time instructors have bachelor's degrees and the rest have either a master's or doctorate degree.
The part-time instructors come from a variety of employment backgrounds and have different reasons for working part-time.
They may be high school instructors (active or retired), may come from a household in which only one member is working full time while the other teaches part time, may be recently graduated MS or MAT students seeking full time employment, may be working full time elsewhere in a non-educational field, or may be retired from a non-educational field (see
\vref{app:sec:facultyDegrees}).
%  Is it true that a quarter of our PT faculty only have BS degrees?  How did
%  this happen?  I don't see room for that in the IQs.  How did you get this
%  data?

\subsection[Faculty diversity]{
    How the faculty composition reflects the diversity and cultural competency goals of the institution.
}
The mathematics SAC is deeply committed to fostering an inclusive campus climate at each location that respects all individuals regardless of race, color, religion, ethnicity, use of native language, national origin, sex, marital status, height/weight ratio, disability, veteran status, age, or sexual orientation.
Many of these human characteristics noted above are not measurable nor necessarily discernible.
However, PCC does gather data on gender and race/ethnicity, as detailed in \cref{reflect:tab:racialethnicmakeup}
(see also the extensive demographic data displayed in
\vref{app:sec:demographicdata}).

\begin{table}[!htb]
    \centering
    \caption{Racial/Ethnic Make-up of PCC Faculty and Students}
    \label{reflect:tab:racialethnicmakeup}
    \begin{tabular}{rrrr}
        \toprule
                                  & PT Faculty & FT Faculty & Students \\
        \midrule
        Male                      & 54.1\%     & 53.2\%     & 55\%     \\
        Female                    & 45.9\%     & 47\%       & 45\%     \\
        Asian /Pacific Islander   & 7.7\%      & 6.4\%      & 8\%      \\
        Black or African American & 1.1\%      & 0.0\%      & 6\%      \\
        Hispanic/Latino           & 2.2\%      & 4.3\%      & 11\%     \\
        Multiracial               & 1.1\%      & 0.0\%      & 3\%      \\
        Native American           & 0.0\%      & 0.0\%      & 1\%      \\
        Unknown/International     & 12.2\%     & 4.3\%      & 3\%      \\
        Caucasian                 & 75.7\%     & 85.1\%     & 68\%     \\
        \bottomrule
    \end{tabular}
\end{table}

Our SAC will continue to strive toward keeping our faculty body ethnically diverse and culturally competent, but it is an area where improvement is needed.
In terms of hiring, there is a shortage of minorities in the Science, Technology, Engineering and Mathematics (STEM) undergraduate and graduate programs, which makes our recruitment of minority faculty difficult. \label{reflect:page:stem}

\recommendation[Math SAC, Division Deans]{
    Math chairs and deans should strongly recommend that full- and part-time faculty attend workshops related to diversity and cultural competency issues.
}

\recommendation[PCCFFAP, Division Deans]{
    Part-time faculty should be allowed to attend diversity/cultural awareness workshops in lieu of contractually mandated quarterly meetings.
}

\recommendation[Math SAC, Division Deans, Human Resources]{
    Hiring committees need to work with HR to identify and aggressively target mathematics graduate programs in the Northwest with minority students who are seeking teaching positions in community colleges.
}

\recommendation[Division Deans, Faculty Department Chairs]{
    Departments on all campuses should increase efforts to find candidates for the Faculty Diversity Internship Program \cite{affirmativeaction}.
}

\section[Changes to instructor qualifications]{
    Report any changes the SAC has made to instructor qualifications since the last review and the reason for the changes.
}
In Spring 2011, prompted by the transfer of MTH 20 from Developmental Education (DE) to the Mathematics SAC, the math instructor qualifications were changed.
MTH 20 had been the only remaining mathematics course in the DE SAC.

The transfer included transitioning three full-time DE math instructors at Sylvania into the Math Department at Sylvania.
At this time, instructor qualifications for math faculty were examined and changed to reflect the inclusion of DE math faculty.
It was determined that separate qualifications should be written for pre-college and college level courses.
These qualifications were written so that all of the full-time DE math faculty transitioning into the math department (as well as any new DE math faculty hired) were qualified to teach the pre-college level courses and any new math faculty were qualified to teach all of the math courses.

For instance, a masters degree in mathematics education (instead of just mathematics) was included as an optional qualification for full-time instructors teaching pre-college level courses.
Also a masters degree in mathematics education became an option for part-time instructors teaching MTH 211--213 (the sequence for elementary education math teachers).
Additionally, at the request of the administration, the terms `part-time' and `full-time' were removed from instructor qualifications in order to satisfy accreditation requirements.
Instead of labeling what had traditionally been part-time qualifications as `part-time,' these qualifications were labeled `Criteria for Provisional Instructors.'

In Winter 2013, the math instructor qualifications were again changed at the request of the math department chairs.
The `provisional' labeling from the last revision had required math department chairs to regularly re-certify part-time (`provisional') instructors.
In order to avoid this unnecessary paperwork, the SAC adopted a three-tiered qualification structure based on full-time, part-time, and provisionally-approved part-time instructors (mainly graduate students currently working on graduate degrees).
The part-time (non-provisional) tier was labeled `Demonstrated Competency.' Complete details of instructor qualifications are given in \vref{app:sec:instructorquals}.

\section[Professional development activities]{
    How have professional development activities of the faculty contributed to the strength of the program/discipline?
    If such activities have resulted in instructional or curricular changes, please describe.
}

The members of the mathematics SAC, full-time and part-time alike, are very committed to professional development.
As with members of any academic discipline, the faculty in the Math SAC pursue professional development in a variety of manners.
Traditionally these activities have been categorized in ways such as `membership in professional organizations' or `presentations at conferences'.
The members of the Math SAC do not in any way devalue the engagement in such organizations or activities, and in fact a summative list of such things can be found in \vref{app:sec:memberships}.

Nor do the members in any way diminish individual pursuit of professional development.
In an attempt to acknowledge such pursuits, each member of the full-time faculty was asked to submit one or two highlights of their professional development activities over the past five years.
Those submissions can be found in \vref{app:sec:professionaldevelop}.

It should be noted that the list of organizations and activities found in these appendices are not exhaustive; they are merely a representative sample of the types of professional development pursuits engaged in by members of the Math SAC.

The members of the Math SAC realize that if there is going to be institutional-level change that results in increased success and completion rates for students enrolled in DE mathematics courses, there are going to have to be targeted and on-going professional development activities with that goal in mind and that all mathematics faculty, full-time and part-time, are going to have to take advantage of those opportunities.
This is especially important since many of our faculty members are not specialists in working with developmental mathematics students.
We look forward to working with the broader PCC community as we pursue our common goal of increased student success and completion, and we look forward to the college's support in providing professional development opportunities that promote attainment of this goal.

\recommendation[PCC Cabinet]{
    The college should provide funds and other necessary resources that allow the SAC members to engage in targeted, on-going professional development geared toward realization of district-wide goals.
    This should include, for example, support for activities such as annual two-day workshops focusing on goals such as universal adoption of evidence-based best practices.
}

\recommendation[Division Deans, Faculty Department Chairs, PCCFFAP, Completion Investment Council]{
    Each math department should create structures and policies that promote sustained professional development.
    Institutionalization of practices such as faculty-inquiry-groups and peer-to-peer classroom visitations are necessary components of sustained professional development.
}

\recommendation[Math SAC, PCC Cabinet]{
    The college should continue to provide funds for activities such as conference attendance, professional organization membership, etc.
    At the same time, procedures should be put into place that allow for maximal dissemination of ``good ideas'' and maximum probability that said ideas grow into sustained practices.
}

\recommendation[Division Deans, Faculty Department Chairs, PCCFFAP]{
    Formalized procedures for mentoring new faculty, full-time and part-time alike, should be adopted and strictly observed.
    Beginning a new job is a unique opportunity for rapid professional development, and we need to make sure that we provide as supportive and directed an opportunity for new faculty as possible so that the development happens in a positive and long-lasting way.
}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_sentence_across_blocks(self):
        text = r"""
This sentence stretches
\[
  x^2
  \]
across lines.

As does
\begin{tabular}{cc}
  1 & 2\\
3&4\end{tabular}
this one.
        """

        formatted = r"""
This sentence stretches
\[
    x^2
\]
across lines.

As does
\begin{tabular}{cc}
    1 & 2 \\
    3 & 4
\end{tabular}
this one.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_six_sentences_mutl_blank(self):
        text = r"""
This is the first
sentence. This is the second sentence. This is the
third sentence.



This is the fourth
sentence!



This is the fifth
sentence. This is the
sixth sentence.


This is the seventh
sentence! This is the
eighth sentence.

This is the ninth
sentence? This is the
tenth sentence.
\par
This is
the eleventh
sentence.
        """

        formatted = r"""
This is the first sentence.
This is the second sentence.
This is the third sentence.

This is the fourth sentence!

This is the fifth sentence.
This is the sixth sentence.

This is the seventh sentence!
This is the eighth sentence.

This is the ninth sentence?
This is the tenth sentence.
\par
This is the eleventh sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_textbook_snippet(self):
        """
        Difference: the double dollar signs have been removed.
        """

        text = r"""
% https://tex.stackexchange.com/questions/325505/best-practices-for-source-file-line-lengths/325511
This manual is intended for people who have never used \TeX\ before, as
well as for experienced \TeX\ hackers. In other words, it's supposed to
be a panacea that satisfies everybody, at the risk of satisfying nobody.
Everything you need to know about \TeX\ is explained
here somewhere, and so are a lot of things that most users don't care about.
If you are preparing a simple manuscript, you won't need to
learn much about \TeX\ at all; on the other hand, some
things that go into the printing of technical books are inherently
difficult, and if you wish to achieve more complex effects you
will want to penetrate some of \TeX's darker corners. In order
to make it possible for many types of users to read this manual
effectively, a special sign is used to designate material that is
for wizards only: When the symbol
\vbox{\hbox{\dbend}\vskip 11pt}
appears at the beginning of a paragraph, it warns of a ``^{dangerous bend}''
in the train of thought; don't read the paragraph unless you need to.
Brave and experienced drivers at the controls of \TeX\ will gradually enter
more and more of these hazardous areas, but for most applications the
details won't matter.
        """

        formatted = r"""
% https://tex.stackexchange.com/questions/325505/best-practices-for-source-file-line-lengths/325511
This manual is intended for people who have never used \TeX\ before, as well as for experienced \TeX\ hackers.
In other words, it's supposed to be a panacea that satisfies everybody, at the risk of satisfying nobody.
Everything you need to know about \TeX\ is explained here somewhere, and so are a lot of things that most users don't care about.
If you are preparing a simple manuscript, you won't need to learn much about \TeX\ at all; on the other hand, some things that go into the printing of technical books are inherently difficult, and if you wish to achieve more complex effects you will want to penetrate some of \TeX's darker corners.
In order to make it possible for many types of users to read this manual effectively, a special sign is used to designate material that is for wizards only: When the symbol
\vbox{\hbox{\dbend}\vskip 11pt}
appears at the beginning of a paragraph, it warns of a ``^{dangerous bend}'' in the train of thought; don't read the paragraph unless you need to.
Brave and experienced drivers at the controls of \TeX\ will gradually enter more and more of these hazardous areas, but for most applications the details won't matter.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_three_sentences_trailing_comments(self):
        text = r"""
%This is the first
%sentence. This is the second sentence. This is the
%third sentence.

This is the fourth
sentence! This is the fifth sentence? This is the
sixth sentence.
        """

        formatted = r"""
%This is the first
%sentence. This is the second sentence. This is the
%third sentence.

This is the fourth sentence!
This is the fifth sentence?
This is the sixth sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_trailing_comments(self):
        text = r"""
This is %1st comment
the first%    2nd comment
sentence.% 3rd comment

This is the second sentence. %  ?!     4th comment
This is the     % 5th comment
third sentence.

This is the fourth
sentence! This is the fifth sentence? This is the
sixth sentence.
        """

        formatted = r"""
This is %1st comment
the first%    2nd comment
sentence.% 3rd comment

This is the second sentence. %  ?!     4th comment
This is the % 5th comment
third sentence.

This is the fourth sentence!
This is the fifth sentence?
This is the sixth sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_two_sentences(self):
        text = r"""
This is the
first sentence.

This is the second
sentence!
        """

        formatted = r"""
This is the first sentence.

This is the second sentence!
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_verbatim_test(self):
        text = r"""
This is the fourth
sentence! This is the fifth sentence? This is the
sixth sentence, and runs across
\begin{verbatim}
    This is the fourth
        sentence! This is the fifth sentence? This is the
 sixth sentence.
\end{verbatim}
a verbatim environment;
and beyond!

This is the fourth
sentence! This is the fifth sentence? This is the
sixth sentence.
        """

        formatted = r"""
This is the fourth sentence!
This is the fifth sentence?
This is the sixth sentence, and runs across
\begin{verbatim}
    This is the fourth
        sentence! This is the fifth sentence? This is the
 sixth sentence.
\end{verbatim}
a verbatim environment; and beyond!

This is the fourth sentence!
This is the fifth sentence?
This is the sixth sentence.
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


class TestLatexIndentCommands(unittest.TestCase):
    """
    https://github.com/cmhughes/latexindent.pl/blob/main/test-cases/commands
    """

    @unittest.SkipTest
    def test_stars_from_documentation(self):
        """
        TDOO: allow special formatting or use latexindent.pl as plugin
        """

        text = r"""
\newtcolorbox{stars}{%
enhanced jigsaw,
breakable, % allow page breaks
left=0cm,
top=0cm,
before skip=0.2cm,
boxsep=0cm,
frame style={draw=none,fill=none}, % hide the default frame
colback=white,
overlay={
\draw[inner sep=0,minimum size=rnd*15pt+2pt]
decorate[decoration={stars,segment length=2cm}] {
decorate[decoration={zigzag,segment length=2cm,amplitude=0.3cm}] {
([xshift=-.5cm,yshift=0.1cm]frame.south west) --  ([xshift=-.5cm,yshift=0.4cm]frame.north west)
}};
\draw[inner sep=0,minimum size=rnd*15pt+2pt]
decorate[decoration={stars,segment length=2cm}] {
decorate[decoration={zigzag,segment length=2cm,amplitude=0.3cm}] {
([xshift=.75cm,yshift=0.1cm]frame.south east) --  ([xshift=.75cm,yshift=0.6cm]frame.north east)
}};
\node[anchor=north west,outer sep=2pt,opacity=0.25] at ([xshift=-4.25cm]frame.north west) {\resizebox{3cm}{!}{\faGithub}};
},
% paragraph skips obeyed within tcolorbox
parbox=false,
}
        """

        formatted = r"""
\newtcolorbox{stars}{%
    enhanced jigsaw,
    breakable, % allow page breaks
    left=0cm,
    top=0cm,
    before skip=0.2cm,
    boxsep=0cm,
    frame style={draw=none,fill=none}, % hide the default frame
    colback=white,
    overlay={
            \draw[inner sep=0,minimum size=rnd*15pt+2pt]
            decorate[decoration={stars,segment length=2cm}] {
                    decorate[decoration={zigzag,segment length=2cm,amplitude=0.3cm}] {
                            ([xshift=-.5cm,yshift=0.1cm]frame.south west) --  ([xshift=-.5cm,yshift=0.4cm]frame.north west)
                        }};
            \draw[inner sep=0,minimum size=rnd*15pt+2pt]
            decorate[decoration={stars,segment length=2cm}] {
                    decorate[decoration={zigzag,segment length=2cm,amplitude=0.3cm}] {
                            ([xshift=.75cm,yshift=0.1cm]frame.south east) --  ([xshift=.75cm,yshift=0.6cm]frame.north east)
                        }};
            \node[anchor=north west,outer sep=2pt,opacity=0.25] at ([xshift=-4.25cm]frame.north west) {\resizebox{3cm}{!}{\faGithub}};
        },
    % paragraph skips obeyed within tcolorbox
    parbox=false,
}
        """

        ret = texplain.indent(text)
        # import pathlib
        # pathlib.Path('tmp_ret.tex').write_text(ret)
        # pathlib.Path('tmp_formatted.tex').write_text(formatted)
        self.assertEqual(ret.strip(), formatted.strip())

    @unittest.SkipTest
    def test_pstrics1(self):
        """
        TODO: determine what the proper formatting should be
        """

        text = r"""
% arara: indent: {overwrite: true, silent: on}
\documentclass[pstricks]{standalone}
\usepackage{pstricks,multido}

\def\Bottle#1{{\pscustom[linewidth=2pt]{%
                \rotate{#1}
                \psline(-1,3.5)(-1,4)(1,4)(1,3.5)
                \pscurve(3,2)(1,0)\psline(-1,0)
                \pscurve(-3,2)(-1,3.5)}}}

\def\BottleWithWater(#1)#2{%
    \rput[c]{#2}(#1){%
        \rput{*0}(0,0){%
            \psclip{\Bottle{#2}}
            \psframe*[linecolor=gray](-6,-2)(6,2)
            \endpsclip}\rput{*0}(0,0){\Bottle{#2}}}}

\begin{document}

\multido{\iA=-45+5}{19}{%
    \begin{pspicture}(-2.5,-0.5)(6,5.5)
        \BottleWithWater(1.5,1){\iA}
    \end{pspicture}
}

\end{document}
        """

        formatted = r"""
% arara: indent: {overwrite: true, silent: on}
\documentclass[pstricks]{standalone}
\usepackage{pstricks,multido}

\def\Bottle#1{{\pscustom[linewidth=2pt]{%
                \rotate{#1}
                \psline(-1,3.5)(-1,4)(1,4)(1,3.5)
                \pscurve(3,2)(1,0)\psline(-1,0)
                \pscurve(-3,2)(-1,3.5)}}}

\def\BottleWithWater(#1)#2{%
    \rput[c]{#2}(#1){%
        \rput{*0}(0,0){%
            \psclip{\Bottle{#2}}
            \psframe*[linecolor=gray](-6,-2)(6,2)
            \endpsclip}\rput{*0}(0,0){\Bottle{#2}}}}

\begin{document}

\multido{\iA=-45+5}{19}{%
    \begin{pspicture}(-2.5,-0.5)(6,5.5)
        \BottleWithWater(1.5,1){\iA}
    \end{pspicture}
}

\end{document}
        """

        ret = texplain.indent(text)
        # import pathlib
        # pathlib.Path('tmp_ret.tex').write_text(ret)
        # pathlib.Path('tmp_formatted.tex').write_text(formatted)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_multipleBraces(self):
        text = r"""
% arara: indent: {overwrite: yes, trace: on}
\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage}{}{}

\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage}{}{}

\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage}{}{}
        """

        formatted = r"""
% arara: indent: {overwrite: yes, trace: on}
\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage
}{}{}

\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage
}{}{}

\xapptocmd{\tableofcontents}{%
    \end{singlespace}%
    \pagestyle{plain}%
    \clearpage
}{}{}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_issue_379(self):
        text = r"""
\foreach \i/\j in {0.5/$H_{0}$, 1.5/$H_{0}$ } {
        \node at (4.5, -\i) {\j};
    }
    \node[PR] at (3.48, -0.5) {};
         \node[PR] at (3.48, -1.5) {};
    \node[PR] at (3.48, -3.5) {};
        \node[PR] at (3.48, -1.5) {};
        """

        formatted = r"""
\foreach \i/\j in {0.5/$H_{0}$, 1.5/$H_{0}$ } {
    \node at (4.5, -\i) {\j};
}
\node[PR] at (3.48, -0.5) {};
\node[PR] at (3.48, -1.5) {};
\node[PR] at (3.48, -3.5) {};
\node[PR] at (3.48, -1.5) {};
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    @unittest.SkipTest
    def test_isnextchar(self):
        """
                TODO

        Traceback (most recent call last):
          File "/Users/tdegeus/data/prog/src/texplain/tests/test_indent_long.py", line 2565, in test_isnextchar
            ret = texplain.indent(text)
                  ^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 1169, in indent
            text, placeholders_commands = text_to_placeholders(
                                          ^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 891, in text_to_placeholders
            text, placeholders = _detail_text_to_placholders(text, ptype, base, placeholders_comments)
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 713, in _detail_text_to_placholders
            components = find_command(text, is_comment=is_comment)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 337, in find_command
            opts = _find_option(character, index, i_square_open, i_square_closing)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 248, in _find_option
            return _detail_find_option(character, index, braces, [])
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/Users/tdegeus/miniforge3/envs/test/lib/python3.11/site-packages/texplain/__init__.py", line 204, in _detail_find_option
            if np.any(character[index : braces[0]]) and braces[0] - index > 1:
                      ~~~~~~~~~^^^^^^^^^^^^^^^^^^^
        TypeError: slice indices must be integers or None or have an __index__ method
        """

        text = r"""
\parbox{
\@ifnextchar[{\@assignmentwithcutoff}{\@assignmentnocutoff}
}
        """

        formatted = r"""
\parbox{
    \@ifnextchar[{\@assignmentwithcutoff}{\@assignmentnocutoff}
}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


class TestNested(unittest.TestCase):
    def test_nested(self):
        text = r"""
\renewcommand{\maketitle}{%
    \newpage
    \null
    \vskip 2em%
    \begin{center}%
        \let \footnote \thanks
        {\Large\bfseries \@title \par}%
        \vskip 1.5em%
        {\normalsize
            \lineskip .5em%
            \begin{tabular}[t]{c}%
                \@author
        \end{tabular}\par}%
        \vskip 0.5em%
        {\small \@date}%
    \end{center}%
    \par
    \vskip 1.5em
    \thispagestyle{fancy}
}
        """

        formatted = r"""
\renewcommand{\maketitle}{%
    \newpage
    \null
    \vskip 2em%
    \begin{center}%
        \let \footnote \thanks
        {\Large\bfseries \@title \par}%
        \vskip 1.5em%
        {
            \normalsize
            \lineskip .5em%
            \begin{tabular}[t]{c}%
                \@author
            \end{tabular}
            \par
        }%
        \vskip 0.5em%
        {\small \@date}%
    \end{center}%
    \par
    \vskip 1.5em
    \thispagestyle{fancy}
}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_command_option_only(self):
        text = r"""
\documentclass{goose-article}

\title{General \LaTeX trick: reference to dummy subfigure}
\author{}
\usepackage{kantlipsum}

\begin{document}

\maketitle

See \url{https://tex.stackexchange.com/a/552811/132350} and
\url{https://tex.stackexchange.com/q/612642/132350}.

Here are the references:
to the figure \cref{fig:1}, and to the subfigures \cref{fig:1a} and \cref{fig:1b}.

\begin{figure}[htp]
    \centering
    \subfloat{\label{fig:1a}}
    \subfloat{\label{fig:1b}}
    \includegraphics[width=.4\linewidth]{example-image-a}
    \hspace{.02\linewidth}
    \includegraphics[width=.4\linewidth]{example-image-b}
    \caption{
        \protect\subref{fig:1a}
        First sub caption.
        \protect\subref{fig:1b}
        Second sub caption.
        \kant[8]
    }
    \label{fig:1}
\end{figure}

\kant[1-7]

\end{document}
        """

        formatted = r"""
\documentclass{goose-article}

\title{General \LaTeX trick: reference to dummy subfigure}
\author{}
\usepackage{kantlipsum}

\begin{document}

\maketitle

See \url{https://tex.stackexchange.com/a/552811/132350} and
\url{https://tex.stackexchange.com/q/612642/132350}.

Here are the references: to the figure \cref{fig:1}, and to the subfigures \cref{fig:1a} and \cref{fig:1b}.

\begin{figure}[htp]
    \centering
    \subfloat{\label{fig:1a}}
    \subfloat{\label{fig:1b}}
    \includegraphics[width=.4\linewidth]{example-image-a}
    \hspace{.02\linewidth}
    \includegraphics[width=.4\linewidth]{example-image-b}
    \caption{
        \protect\subref{fig:1a}
        First sub caption.
        \protect\subref{fig:1b}
        Second sub caption.
        \kant[8]
    }
    \label{fig:1}
\end{figure}

\kant[1-7]

\end{document}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


class TestAlign(unittest.TestCase):
    def test_align_long(self):
        text = r"""
\begin{tabular}{ccc}
this is the first column with a long text following impeding alignment& and the second column with a long text following impeding alignment& and the third column with a long text following impeding alignment\\
1 &2& 3\\
40 & 50&60
\end{tabular}
        """

        formatted = r"""
\begin{tabular}{ccc}
    this is the first column with a long text following impeding alignment & and the second column with a long text following impeding alignment & and the third column with a long text following impeding alignment \\
    1 & 2 & 3 \\
    40 & 50 & 60
\end{tabular}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


class TestVerbatim(unittest.TestCase):
    def test_verbatim(self):
        text = r"""
\begin{strategy}[H]
    \begin{oframed}
        \caption{Machine-readable names}
        \label{note:misc:strat:names}
Consider making your file- and folder-names machine readable.
For example:
\begin{verbatim}
dimension=2/n=10_dt=0,1/datetime=2023-01-01,12:00:00.h5
\end{verbatim}
is a completely legal name, but you can also read it automatically and interpret it easily by splitting first on the underscore and the slash to separate variables, and then on the equals sign to separate the name from the value.
    \end{oframed}
\end{strategy}
        """

        formatted = r"""
\begin{strategy}[H]
    \begin{oframed}
        \caption{Machine-readable names}
        \label{note:misc:strat:names}
        Consider making your file- and folder-names machine readable.
        For example:
\begin{verbatim}
dimension=2/n=10_dt=0,1/datetime=2023-01-01,12:00:00.h5
\end{verbatim}
        is a completely legal name, but you can also read it automatically and interpret it easily by splitting first on the underscore and the slash to separate variables, and then on the equals sign to separate the name from the value.
    \end{oframed}
\end{strategy}
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_verbatim_a(self):
        text = r'''
\begin{example}[H]
    \begin{oframed}
        \caption{Self-explanatory vs documentation intensive}
        \label{sec:misc:ex:self-explenatory}
        A self-explanatory function might be:
\begin{verbatim}
def area(width: float, height: float) -> float:
    return width * height
\end{verbatim}
        The same function but written in a documentation intensive style might be:
\begin{verbatim}
def property_1(a, b):
    """
    Compute the area of a rectangle.
    :param a: width (scalar)
    :param b: height (scalar)
    :return: area (scalar)
    """
    return a * b
\end{verbatim}
    \end{oframed}
\end{example}
        '''

        formatted = r'''
\begin{example}[H]
    \begin{oframed}
        \caption{Self-explanatory vs documentation intensive}
        \label{sec:misc:ex:self-explenatory}
        A self-explanatory function might be:
\begin{verbatim}
def area(width: float, height: float) -> float:
    return width * height
\end{verbatim}
        The same function but written in a documentation intensive style might be:
\begin{verbatim}
def property_1(a, b):
    """
    Compute the area of a rectangle.
    :param a: width (scalar)
    :param b: height (scalar)
    :return: area (scalar)
    """
    return a * b
\end{verbatim}
    \end{oframed}
\end{example}
        '''

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


class TestCode(unittest.TestCase):
    def test_code(self):
        text = r"""
\if@namecite
    \RequirePackage{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}\raggedright\oldbibliography{#1}\justifying\end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\else
    \RequirePackage[square,sort&compress,numbers,comma]{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}\raggedright\oldbibliography{#1}\justifying\end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\fi
        """

        formatted = r"""
\if@namecite
    \RequirePackage{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}
                \raggedright\oldbibliography{#1}\justifying
            \end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\else
    \RequirePackage[square,sort&compress,numbers,comma]{natbib}
    \let\oldbibliography\bibliography
    \renewcommand{\bibliography}[1]{%
        \setlength{\bibsep}{3pt plus 0.3ex}
        \def\bibfont{\scriptsize}
        \if@twocolumnbib
            \begin{multicols}{2}
                \raggedright\oldbibliography{#1}\justifying
            \end{multicols}
        \else
            \raggedright\oldbibliography{#1}\justifying
        \fi
    }
\fi
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())

    def test_code_a(self):
        text = r"""
\if@narrow
    \RequirePackage[left=40mm, right=40mm, top=30mm, bottom=30mm]{geometry}
\else
    \if@wwide
        \RequirePackage[left=10mm, right=10mm, top=20mm, bottom=20mm]{geometry}
    \else
        \if@wide
            \RequirePackage[left=15mm, right=15mm, top=20mm, bottom=20mm]{geometry}
        \else
            \RequirePackage[left=25mm, right=25mm, top=30mm, bottom=30mm]{geometry}
        \fi
    \fi
\fi
        """

        formatted = r"""
\if@narrow
    \RequirePackage[left=40mm, right=40mm, top=30mm, bottom=30mm]{geometry}
\else
    \if@wwide
        \RequirePackage[left=10mm, right=10mm, top=20mm, bottom=20mm]{geometry}
    \else
        \if@wide
            \RequirePackage[left=15mm, right=15mm, top=20mm, bottom=20mm]{geometry}
        \else
            \RequirePackage[left=25mm, right=25mm, top=30mm, bottom=30mm]{geometry}
        \fi
    \fi
\fi
        """

        ret = texplain.indent(text)
        self.assertEqual(ret.strip(), formatted.strip())


if __name__ == "__main__":
    unittest.main()
