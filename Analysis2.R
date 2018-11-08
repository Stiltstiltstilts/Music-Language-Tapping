library(dplyr)
setwd("/Users/Stilts/Documents/GitHub/Congruency_Music_Language/data")

trial_data          <- read.delim("009trial_log.txt", sep = "\t", header = TRUE)
trial_data$Sentence <- as.character(trial_data$Sentence)
trial_data$Probe    <- as.character(trial_data$Probe)
trial_data$Accuracy <- as.numeric(trial_data$Accuracy)
trial_data$subnum   <- i
#trial_data$subnum   <- as.factor(trial_data$subnum)
trial_data          <- tbl_df(trial_data)

test <- trial_data %>%
  filter(Sentence_extraction != "other", Probe_clause == "main_clause") %>%
  group_by(Congruency, Sentence_extraction) %>%
  summarise(Acc = mean(Accuracy), avg_RT = mean(RT), max_rt = max(RT), min_rt = min(RT))

test_relative <- trial_data %>%
  filter(Sentence_extraction != "other", Probe_clause == "relative_clause") %>%
  group_by(Congruency, Sentence_extraction) %>%
  summarise(Acc = mean(Accuracy), avg_RT = mean(RT), max_rt = max(RT), min_rt = min(RT))
