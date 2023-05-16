# Language - French
# this is used on generated text file
# pre-processing is required on this file - simply go to text file, go to end of file, and hit enter
# then save file
textfile = read.table('sampletexts.txt',sep='\t')
textfile %>% unnest_tokens(input=V1, output="word")
wordcounts <- textfile %>% unnest_tokens(input=V1, output="word") %>% count(word)
wordcloud(wordcounts$word, wordcounts$n)
#ggplot(data=wordcounts) + geom_col(aes(word,n))

# this is used on actual text file
# actual text file is manually created by user - simply download .srt file from youtube
# or simply type subtitles down onto a blank text file
actualtextfile = read.table('actualtext.txt',sep='\t')
actualtextfile %>% unnest_tokens(input=V1, output="word")
actual_wordcounts <- actualtextfile %>% unnest_tokens(input=V1, output="word") %>% count(word)
wordcloud(actual_wordcounts$word, actual_wordcounts$n)

difference_in_files <- anti_join(wordcounts, actual_wordcounts)
# displays differences in received and actual texts, showing how many "mistakes" were made
View(difference_in_files)
