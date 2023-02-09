library(tidyverse)


### Analyzing flocking index

food_data_genes <- read.csv("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/food_full3.txt")
mass_data_genes <- read.csv("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/mass_fish_full3.txt")
n_sharks_data_genes <- read.csv("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/nb_sharks_full3.txt")
regrowth_data_genes <- read.csv("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/regrowth_rate_full3.txt")
reproduction_data_genes <- read.csv("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/reproduction_full3.txt")

all_data <- list(food_data_genes, mass_data_genes, n_sharks_data_genes, regrowth_data_genes, reproduction_data_genes)
plot_names <- c("n_food", "mass", "n_sharks", "regrowth", "reproduction_rate")



for (i in seq_along(all_data)) {
  plot_data <- all_data[[i]]
  plot_title <- plot_names[i]
  plot_data <-  plot_data %>% 
    select(c(ParameterValue, flocking.index)) %>%
    group_by(ParameterValue) %>% 
    summarise(meanflockingIndex = mean(flocking.index),
              sdFlockingIndex = sd(flocking.index)) %>% 
    ungroup()
  
  png(paste0(plot_title, "_flocking.png"), width = 500, height = 500)
  p <- .plotting_function_flocking(plot_data, plot_title)
  print(p)
  dev.off()
}

.plotting_function_flocking <- function(plot_data, plot_title) {
  p <- ggplot(data = plot_data, mapping = aes(x = ParameterValue, y = meanflockingIndex)) +
    geom_point(size = 1) +
    geom_line() +
    geom_errorbar(aes(ymin = meanflockingIndex - 1.96 * sdFlockingIndex, ymax = meanflockingIndex + 1.96 * sdFlockingIndex)) +
    theme_light() +
    ggtitle(plot_title) +
    xlab(paste(plot_title, "Parameter")) +
    ylab("Flocking Index")
  
  return(p)
}



for (i in seq_along(all_data)) {
  plot_data <- all_data[[i]]
  plot_title <- plot_names[i]
  plot_data <-  plot_data %>% 
    select(c(ParameterValue, number_fish)) %>%
    group_by(ParameterValue) %>% 
    summarise(meanNumber = mean(number_fish),
              sdNumber = sd(number_fish)) %>% 
    ungroup()
  
  png(paste0(plot_title, "_n_fish.png"), width = 500, height = 500)
  p <- .plotting_function_n_fish(plot_data, plot_title)
  print(p)
  dev.off()
}

.plotting_function_n_fish <- function(plot_data, plot_title) {
  p <- ggplot(data = plot_data, mapping = aes(x = ParameterValue, y = meanNumber)) +
    geom_point(size = 1) +
    geom_line() +
    geom_errorbar(aes(ymin = meanNumber - 1.96 * sdNumber, ymax = meanNumber + 1.96 * sdNumber)) +
    theme_light() +
    ggtitle(plot_title) +
    xlab(paste(plot_title, "Parameter")) +
    ylab("Number of Fish")
  
  return(p)
}


### Analyzing Genes

for (i in seq_along(all_data)) {
  plot_data <- all_data[[i]]
  plot_title <- plot_names[i]
  plot_data <-  plot_data %>% 
    select(c(ParameterValue, Gene0_avg, Gene1_avg, Gene2_avg, Gene3_avg, Gene4_avg)) %>%
    group_by(ParameterValue) %>% 
    summarise(Align = mean(Gene0_avg),
              Separate = mean(Gene1_avg),
              Cohesion = mean(Gene2_avg),
              Predator = mean(Gene3_avg),
              Food = mean(Gene4_avg)) %>% 
    ungroup() %>%
    pivot_longer(cols = c(Align, Separate, Cohesion, Predator, Food), names_to = "Gene", values_to = "Weight") %>% 
    as.data.frame()
    

  
  png(paste0(plot_title, "_genes.png"), width = 500, height = 500)
  p <- .plotting_function_genes(plot_data, plot_title)
  print(p)
  dev.off()
}

.plotting_function_genes <- function(plot_data, plot_title) {
  p <- ggplot(data = plot_data, mapping = aes(x = ParameterValue, y = Weight, fill = Gene)) +
    geom_bar(position="fill", stat="identity") +
    ggtitle(plot_title) +
    theme_light()
  return(p)
}
