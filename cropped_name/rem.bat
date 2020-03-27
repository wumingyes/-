rem 执行改批处理前先要目录下创建font_properties文件

echo Run Tesseract for Training..

tesseract.exe mychi.font.exp0.tif mychi.font.exp0 -l chi_sim --psm 6 nobatch box.train

echo Compute the Character Set..

unicharset_extractor.exe mychi.font.exp0.box

mftraining -F font_properties -U unicharset -O mychi.unicharset mychi.font.exp0.tr

echo Clustering..

cntraining.exe mychi.font.exp0.tr

echo Rename Files..

rename normproto mychi.normproto

rename inttemp mychi.inttemp

rename pffmtable mychi.pffmtable

rename shapetable mychi.shapetable

echo Create Tessdata..

combine_tessdata.exe mychi.