\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ccu-thesis}[2026/09/24 CCU thesis]
\LoadClass[12pt,a4paper,twoside,openany,leqno]{book}
\RequirePackage{iftex}
\RequireXeTeX
\RequirePackage{etoolbox}
\input{thesis-config.tex}
\RequirePackage{fontspec,xeCJK}
\xeCJKsetup{PunctStyle=plain}
% Fail on missing prescribed fonts; never silently substitute another Kai font.
\IfFontExistsTF{\ThesisLatinFont}{}{\ClassError{ccu-thesis}{Times New Roman not found}{Install the licensed font before compiling.}}
\setmainfont{\ThesisLatinFont}
\setsansfont{\ThesisLatinFont}
\ifdefempty{\ThesisCJKFontFile}{
  \IfFontExistsTF{\ThesisCJKFont}{}{\ClassError{ccu-thesis}{Required DFKai-SB font not found}{Install licensed DFKai-SB or set ThesisCJKFontFile.}}
  \setCJKmainfont[AutoFakeBold=2,AutoFakeSlant=.2]{\ThesisCJKFont}
  \setCJKsansfont[AutoFakeBold=2,AutoFakeSlant=.2]{\ThesisCJKFont}
}{
  \setCJKmainfont[AutoFakeBold=2,AutoFakeSlant=.2]{\ThesisCJKFontFile}
  \setCJKsansfont[AutoFakeBold=2,AutoFakeSlant=.2]{\ThesisCJKFontFile}
}
\RequirePackage[margin=20mm,headheight=0pt,headsep=0pt,footskip=10mm]{geometry}
\RequirePackage{fix-cm}
\RequirePackage[leqno]{amsmath}
\RequirePackage{amssymb,graphicx,xcolor}
\RequirePackage{titlesec,tocloft,caption,zhnumber,pdfpages,eso-pic}
\RequirePackage[unicode,hidelinks,bookmarksnumbered]{hyperref}
\RequirePackage{bookmark}
\RequirePackage{ccu-bibliography}
\renewcommand{\normalsize}{\fontsize{12bp}{18bp}\selectfont}
\renewcommand{\small}{\fontsize{10bp}{15bp}\selectfont}
\AtBeginDocument{\normalsize}
\setlength{\parindent}{24bp}
\setlength{\parskip}{0pt}
\setlength{\emergencystretch}{1em}
\raggedbottom
\pagestyle{empty}
\newif\ifccuwatermark
\newif\ifccufooter
\ccufootertrue
\ccuwatermarkfalse
% Distance is to the footer baseline, following the Word footer setting.
\AddToShipoutPictureFG{
  \ifccufooter
    \AtPageLowerLeft{\raisebox{10mm}[0pt][0pt]{%
      \makebox[\paperwidth]{\fontsize{12bp}{18bp}\selectfont\thepage}}}
  \fi
}
\AddToShipoutPictureBG{
  \ifccuwatermark
    \AtPageCenter{\makebox[0pt]{\raisebox{-.5\height}{%
      \includegraphics[width=\ThesisWatermarkWidth]{\ThesisWatermarkFile}}}}
  \fi
}
\def\ThesisUniversity{國立中正大學}
\ifdefstring{\ThesisProgram}{im}{\def\ThesisInstitute{資訊管理研究所}}{
  \ifdefstring{\ThesisProgram}{him}{\def\ThesisInstitute{醫療資訊管理研究所}}{
    \ClassError{ccu-thesis}{Unknown ThesisProgram}{Use im or him.}
  }
}
\ifdefstring{\ThesisMode}{proposal}{
  \def\ThesisDocumentName{\ThesisDegree 論文提案書}
}{
  \ifdefstring{\ThesisMode}{thesis}{\def\ThesisDocumentName{\ThesisDegree 論文}}{
    \ClassError{ccu-thesis}{Unknown ThesisMode}{Use thesis or proposal.}}
}
\newcommand{\ccuchapterlabel}{第\zhnumber{\arabic{chapter}}章}
\titleformat{\chapter}[block]
  {\centering\bfseries\fontsize{18bp}{27bp}\selectfont}
  {\ccuchapterlabel、}{0pt}{}
\newlength{\ccuchapterafter}
\setlength{\ccuchapterafter}{\dimexpr18bp*\ThesisChapterAfterLines\relax}
\titlespacing{\chapter}{0pt}{0pt}{\ccuchapterafter}
\assignpagestyle{\chapter}{empty}
\titleformat{\section}[block]
  {\bfseries\fontsize{14bp}{21bp}\selectfont}{\thesection}{.5em}{}
\titlespacing{\section}{0pt}{36bp}{18bp}
\titleformat{\subsection}[block]
  {\bfseries\fontsize{12bp}{18bp}\selectfont}{\thesubsection}{.5em}{}
\titlespacing{\subsection}{0pt}{36bp}{18bp}
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{2}
\RequirePackage{indentfirst}
\renewcommand{\contentsname}{目錄}
\renewcommand{\listfigurename}{圖目錄}
\renewcommand{\listtablename}{表目錄}
\renewcommand{\figurename}{圖}
\renewcommand{\tablename}{表}
\renewcommand{\bibname}{參考文獻}
\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\cftchappagefont}{\normalfont}
\renewcommand{\cftchappresnum}{}
\renewcommand{\cftchapaftersnum}{}
\setlength{\cftchapnumwidth}{4.5em}
\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}}
\setlength{\cftbeforechapskip}{0pt}
\setlength{\cftsecindent}{1em}
\setlength{\cftsubsecindent}{2em}
\setlength{\cftsecnumwidth}{2.5em}
\setlength{\cftsubsecnumwidth}{3.5em}
\renewcommand{\cftfigpresnum}{圖 }
\renewcommand{\cftfigaftersnum}{：}
\renewcommand{\cfttabpresnum}{表 }
\renewcommand{\cfttabaftersnum}{：}
\setlength{\cftfigindent}{0pt}
\setlength{\cfttabindent}{0pt}
\setlength{\cftfignumwidth}{4.5em}
\setlength{\cfttabnumwidth}{4.5em}
\setlength{\cftbeforefigskip}{0pt}
\setlength{\cftbeforetabskip}{0pt}
\makeatletter
\let\ccu@original@lchapter\l@chapter
\renewcommand{\l@chapter}[2]{%
  \begingroup
  \let\ccu@original@numberline\numberline
  \renewcommand{\numberline}[1]{\ccu@original@numberline{第\zhnumber{##1}章、}}%
  \ccu@original@lchapter{#1}{#2}%
  \endgroup
}
\newcommand{\ccucontents}{
  \chapter*{\contentsname}
  \addcontentsline{toc}{chapter}{\contentsname}
  \@starttoc{toc}
  \chapter*{\listfigurename}
  \addcontentsline{toc}{chapter}{\listfigurename}
  \@starttoc{lof}
  \chapter*{\listtablename}
  \addcontentsline{toc}{chapter}{\listtablename}
  \@starttoc{lot}
}
\makeatother
\DeclareCaptionFont{ccusize}{\fontsize{12bp}{18bp}\selectfont}
\captionsetup{font=ccusize,labelfont=bf,textfont=it,labelsep=newline,
  justification=raggedright,singlelinecheck=false,skip=6bp}
\numberwithin{equation}{chapter}
\newcommand{\ccunote}[1]{\par{\raggedright\fontsize{10bp}{15bp}\selectfont\itshape\noindent 註：#1\par}}
\newcommand{\ccusource}[1]{\par{\raggedright\fontsize{10bp}{15bp}\selectfont\noindent 參考文獻：#1\par}}
\newcommand{\ccueqref}[1]{\mbox{（\ref{#1}）}}
\newcommand{\ccumakecover}{
  \pagenumbering{roman}
  \ccuwatermarkfalse
  \thispagestyle{empty}
  \begingroup
  \centering
  \vspace*{8mm}
  {\fontsize{36bp}{54bp}\selectfont\bfseries \ThesisUniversity\par}
  {\fontsize{\ThesisCoverOtherSize bp}{36bp}\selectfont
    \ThesisInstitute\par
    \ThesisDocumentName\par
    \vspace{36bp}
    \ThesisTitleZh\par
    \ThesisTitleEn\par
    \vfill
    研究生：\ThesisAuthor\quad 撰\par
    指導教授：\ThesisAdvisor\quad \ThesisAdvisorTitle\par
    \vspace{26mm}
    中華民國 \ThesisROCYear\ 年 \ThesisMonth\ 月\par
  }
  \vspace*{8mm}
  \endgroup
  \clearpage
}
\newcommand{\ccuapproval}{
  \ccuwatermarkfalse
  \ifdefempty{\ThesisApprovalPDF}{
    \chapter*{論文口試委員會審定書}
    \begin{center}\textbf{【佔位頁，非校方正式審定書】}\end{center}
    本頁僅供版型及頁序驗證。請使用學校提供的正式審定書，
    完成口試委員簽章後，將掃描 PDF 路徑填入基本資料設定檔。
    正式送印及繳交前必須替換本頁。
    \vspace{18mm}
    \begin{center}
      \fbox{\begin{minipage}[c][100mm][c]{.88\textwidth}
      \centering 正式審定書與委員簽章 PDF 預留區
      \end{minipage}}
    \end{center}
    \clearpage
  }{
    \includepdf[pages=-,pagecommand={\thispagestyle{empty}},fitpaper=false]{\ThesisApprovalPDF}
  }
}
\newcommand{\ccufrontmatter}{
  \ifdefstring{\ThesisMode}{thesis}{
    \ccuapproval
    \ccuwatermarktrue
    \chapter*{誌謝}\input{frontmatter/acknowledgements.tex}
    \chapter*{摘要}\input{frontmatter/abstract-zh.tex}
    \chapter*{Abstract}\input{frontmatter/abstract-en.tex}
  }{\ccuwatermarktrue}
  \ccucontents
  \clearpage
  \pagenumbering{arabic}
}
\newcommand{\ccuappendices}{
  \appendix
  \renewcommand{\ccuchapterlabel}{附錄 \Alph{chapter}}
  \renewcommand{\theequation}{\Alph{chapter}-\arabic{equation}}
}
\newcommand{\ccuappendix}[1]{
  \clearpage
  \refstepcounter{chapter}
  \chapter*{附錄 \Alph{chapter}：#1}
  \addcontentsline{toc}{chapter}{附錄 \Alph{chapter}：#1}
}
\newcommand{\ccubackcover}{
  \clearpage
  \ccuwatermarkfalse
  \ccufooterfalse
  \thispagestyle{empty}\null\clearpage
}
