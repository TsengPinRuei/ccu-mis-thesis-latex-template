# 編譯與格式驗證紀錄

驗證日期：2026-09-24。頁碼來源均指 format.pdf 的 **PDF 實體頁碼**。
需求判讀及三項使用者裁定見 [format-requirements.md](format-requirements.md)；
以下紀錄只適用於本次交付的佔位示例，不能替代使用者正式論文的最終校對。

## 成果與驗證方法

| 成果 | 實際頁數 | 印出頁碼與組成 |
| --- | ---: | --- |
| ../output/pdf/main.pdf | 14 | 封面 i、審定佔位 ii、誌謝 iii、摘要 iv、Abstract v、目錄 vi、圖目錄 vii、表目錄 viii；正文 1–2、文獻 3、附錄 4–5，最後為無號空白封底 |
| ../output/pdf/proposal.pdf | 10 | 封面 i、目錄 ii、圖目錄 iii、表目錄 iv；正文 1–2、文獻 3、附錄 4–5、空白封底 |
| ../output/pdf/spine.pdf | 1 | 15 × 297 mm 直排書背，無頁碼；15 mm 是可調整的裝訂預設 |

使用 XeLaTeX（TeX Live 2025）及 Biber 2.21。
論文與提案均完成 XeLaTeX → Biber → XeLaTeX → XeLaTeX；
書背完成 XeLaTeX 編譯。最終 .log／.blg 未見警告、錯誤、缺字、溢出或未解決引用。
編譯腳本的 shell 語法檢查亦通過。

完整閱讀來源 18 頁文字及全部頁面影像，包含圖 1–8、封面及各前置頁／正文範例。
輸出使用 Poppler 渲染，主論文 14 頁、提案 10 頁及書背 1 頁全部目視；
修正後重新檢視受影響的圖表、公式、附錄頁。沒有發現裁切、重疊、缺字、壞掉的引用或意外空白頁。

[validation-metrics.json](validation-metrics.json) 保存三份最終 PDF 的 SHA-256、
逐項座標、字級、字型嵌入及頁碼等量測證據。
[scripts/verify_pdf.py](../scripts/verify_pdf.py) 的 **50 項自動檢查全數通過，0 項失敗**；
7 個人工檢查標記保留為人工項，沒有偽裝為自動通過。
其中版面目視、標題間距判讀及斜體外框檢查已在本次人工檢視完成；
實際裝訂仍待使用者處理。

可重跑：

~~~sh
bash scripts/build.sh
bash scripts/build.sh proposal
bash scripts/build.sh spine
python3 scripts/verify_pdf.py --report docs/validation-metrics.json
~~~

改正文後，腳本中的示例文字定位可能需要調整；報告裡的雜湊可用來辨認驗證的是哪一版 PDF。

## 格式符合性對照表

「已驗證」表示指定的程式實作與本次示例 PDF 有證據支持；
「示例／預設」表示不是來源明定的數值；
「人工」表示不能由模板完成或來源未提供正式材料。

| 規定／採用方式 | format.pdf 頁碼 | 實作位置 | 本次驗證結果 |
| --- | --- | --- | --- |
| 兩所正式名稱；碩士論文及提案 | 5、9 | thesis-config.tex、ccu-thesis.cls 所別／模式判斷、proposal.tex | 已驗證資訊管理論文／提案；另編譯 medical 設定，封面正確顯示醫療資訊管理研究所 |
| 文件完整組成及順序 | 1 | main.tex、\ccufrontmatter、\ccubackcover | 已逐頁驗證，文獻在附錄前；圖6不一致的示意順序沒有套入 |
| 提案免審定、誌謝與兩摘要 | 1 | \ccufrontmatter | proposal.pdf 10 頁實證確認省略 |
| 每個組成項目及各章換新頁 | 3 | book openany、\chapter、\ccuappendix | 已驗證；沒有非必要奇數頁補白 |
| A4 | 原檔實體尺寸 | geometry a4paper | 示例／預設：主檔與提案全頁 595.276 × 841.890 bp（210 × 297 mm） |
| 四邊留邊 2 cm | 2 圖1、4 | ccu-thesis.cls geometry margin=20mm | 版心與文字排版寬度已量測；正文／圖表無實質越界，斜體字型外框差異另見下段 |
| 頁碼置中，距底 1 cm | 2 | \AddToShipoutPictureFG | 所有有號頁的基線距底約 10.0001 mm，水平中心誤差小於 0.1 bp |
| 標楷體／Times New Roman | 1 | fontspec、xeCJK 設定 | PDF 已嵌入 DFKaiShu-SB、TimesNewRomanPSMT／BoldMT／ItalicMT；逐字檢查中文及非數學英文的實際字型 |
| 正文 12 點 | 1 | \normalsize | PDF 字級 12.000 bp；沒有把 LaTeX 傳統 pt 當成 Word 點 |
| 行距 1.5 | 2、17 | \fontsize{12bp}{18bp} | 數值化預設為 18 bp；實測正文連續行及跨段落基線差 18.000 bp |
| 左右對齊、段落 | 3、17 | TeX 段落、parindent／parskip、PunctStyle=plain | 目視長段落已左右對齊；兩字段首縮排為示例預設，實測 24.0001 bp；段間無額外空行 |
| 中文正文全形／表格及英文半形括號 | 3 | 範例內容、\ccucite、\ccueqref | 本次示例已人工校對；公式引用不跨行。新增文字仍須作者校對 |
| 不放題目姓名章節頁眉／頁尾 | 3 | pagestyle empty、獨立頁碼 | 全頁已驗證僅頁碼 |
| 淡色圖片浮水印 | 3、7、9–18 | assets/watermark.png、shipout 背景 | 原 PDF 圖像擷取，已淡藍；主檔 iii 至正文末、提案目錄起使用；封面、審定及封底不加，逐頁圖像存在性及目視均確認 |
| 章／節／小節粗體 18／14／12 | 1 示例 | titleformat | 採示例；PDF 字級實測 18／14／12，目視粗體及置中／左對齊 |
| 章後兩行；節前兩行、節後一行 | 1、3、17 | titlespacing、ccuchapterafter | 依使用者裁定，間距膠為 36／36／18 bp；目視及座標量測完成，基線差包含字型與 strut，非直接當空行高度 |
| 封面校名粗體36，其餘24，欄位排列 | 5、9 | \ccumakecover、thesis-config.tex | 依使用者裁定；所有欄位實測36或24 bp，中英題目、作者、教授、民國年月順序及置中已目視 |
| 正式審定書 | 5 | \ccuapproval、ThesisApprovalPDF | 匯入入口以 A4 測試 PDF 驗證；交付示例保留清楚標記佔位，官方格式及簽章未提供，需人工替換 |
| 摘要及各目錄標題18點、內文同正文 | 5、10–16 | \chapter*、frontmatter/、\ccucontents | 字級量測與目視完成；誌謝同樣式為合理預設 |
| 目錄層級、點線、頁碼右對齊 | 6–7、13–16 | tocloft、\ccucontents | 章節及圖表條目生成成功，最右頁碼邊界 538.582 bp；自列目錄，頁次與實體內容相符 |
| 前置i起連續；正文1起至附錄 | 1，對照9–18 | pagenumbering roman／arabic | 使用者裁定已實作；主檔 i–viii、1–5；提案 i–iv、1–5 |
| 圖下圖號及斜體題、表上表號及斜體題 | 4 | caption、chapters/ 範例 | 圖／表順序、字級及對齊已量測與目視；圖框與圖題左界一致 |
| 註10點斜體、完整來源10點，置下 | 4 | \ccunote、\ccusource、\fullcite | 全部10.000 bp；註與來源靠左，表來源為完整書目而非僅作者年 |
| 圖表章別編號 | 4、7、15–16 | book 計數器、caption、tocloft | 示例採圖1.1、表2.1；正文引用與目錄一致 |
| 公式編號左靠版心 | 5 | amsmath leqno | (2.1)、(A-1)、(A-2)、(B-1) 起點皆約56.693 bp＝20 mm |
| 附錄 A/B，公式 A-1 起算，頁碼延續 | 1、6 | \ccuappendices、\ccuappendix | A-1、A-2、B-1及4、5頁均正確；附錄錨點已檢查落在實體第12、13頁 |
| APA7 文獻樣式 | 6 | ccu-bibliography.sty、biblatex-apa | 已編譯與檢查書籍、期刊示例，年份、作者、題名、卷期、頁碼、英文斜體及懸掛縮排正常；不能替所有文獻型別／真實性背書 |
| 文內英先中後，文末中先英後及筆畫／字母排序 | 6 | sorting=ccu、keywords／sortkey、\ccureferences | 亂序輸入後引文 Adams→Brown→王→林；文末王→林→Adams→Brown；中文排序碼需作者人工維護 |
| 直排書背 | 6、8 | spine.tex、書背設定 | 一頁15×297 mm，級別→學校所別→文件名→題目→作者→撰，無溢出；實體寬度需裝訂店確認 |
| 封底 | 1 | \ccubackcover | 採無字空白預設；無字、無頁碼、無浮水印已量測 |
| 雙面列印 | 6 | twoside、README 送印說明 | 數位排版已實作；實際印表機雙面長邊翻頁與裝訂需人工 |

## 量測判讀與限制

- 1.5 行高採12點乘1.5＝18 bp基線距，是明示的操作性解釋。來源沒有提供
  Word 每個字型的完整行距演算法，不宣稱與任何 Word 安裝環境的自動行高逐像素相同。
- 標題的實測章→首節基線差為59.790 bp、節→正文為36.000 bp；它們包含字級、
  字型與 strut 高度。實作的空白間距以12點字、1.5行高為單位，另搭配頁面影像判定。
- 中文粗體、斜體從同一標楷體人工加粗／傾斜；不是假稱有原生標楷體粗斜體字檔。
  英文使用真正 TNR 粗體及斜體。數學符號採 Computer Modern，是來源未指定部分的預設。
- pdfplumber 的「斜體字型字格矩形」可比其文字排版寬度多出約0.40–1.92 bp，
  並不等於實際墨跡輪廓。報告完整保留這些矩形的座標與 shear。
  本次文字起點＋advance 均在版心內，已目視相關圖題、註與文獻，未見裁切／重疊；
  不把所有斜體矩形均在2cm內當成已通過的項目。
- PDF 引用連結的目標已讀取：兩章、圖表、公式及文獻均指向對應頁；
  附錄 A/B 的命名錨點在最後修正後落在第12／13頁。目錄編譯沒有未定義引用。
- 醫療所與正式表單入口另用 tmp/variants/medical.pdf 測試：
  封面顯示「醫療資訊管理研究所」，A4 測試表單插在第2頁並顯示 ii，
  後續頁數14頁及順序保持正確。測試表單明示非正式文件，不含簽章，也不代表學校表單格式驗證。
  測試與渲染暫存檔在完成檢查後已清理；三份成品、編譯紀錄及 JSON 量測報告保留。
- 沒有因工具、字型或編譯環境缺失而未完成的數位示例檢查。
  **未完成的人工事項**為正式審定書內容及簽章、個人資料／文獻真實性、
  實際雙面列印、書背最終寬度及紙本裝訂；詳細操作已寫 README。
- **沒有尚待裁定的來源衝突**。三項有矛盾的來源已依使用者答覆實作，
  但這是本次採用政策，不能宣稱來源原本毫無矛盾。
