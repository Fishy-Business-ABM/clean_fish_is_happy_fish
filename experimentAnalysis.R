library(tidyverse)


### Analyzing clustering coefficient

food_data <- read.delim("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/food.txt")
mass_data <- read.delim("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/mass_fish.txt")
n_sharks_data <- read.delim("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/nb_sharks.txt")
regrowth_data <- read.delim("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/regrowth_rate.txt")
reproduction_data <- read.delim("/Users/Jonee/Documents/GitHub/clean_fish_is_happy_fish/results/reproduction.txt")

all_data <- list(food_data, mass_data, n_sharks_data, regrowth_data, reproduction_data)

for (i in seq_along(all_data)) {
  plot_data <- all_data[[i]]
  plot_title <- colnames(plot_data)
  plot_data <-  plot_data %>% 
    str_split("\\)") %>%
    unlist() %>% 
    str_split(",") %>% 
    unlist() %>% 
    str_replace_all("\\[", "") %>% 
    str_replace_all("\\(", "") %>% 
    str_replace_all("\\]", "") %>% 
    as.numeric() %>%
    na.omit() %>%  
    matrix(ncol = 3, byrow = TRUE) %>% 
    as.data.frame()
  colnames(plot_data) <- c("Parameter", "Mean", "Var")
  
  png(paste0(plot_title, ".png"), width = 500, height = 500)
  p <- .plotting_function_clustering(plot_data, plot_title)
  print(p)
  dev.off()
}

.plotting_function_clustering <- function(plot_data, plot_title) {
  plot_data <- plot_data %>% 
    mutate(se = sqrt(Var)/sqrt(30)) %>% 
    mutate(CUB = Mean + 1.96 * se, CLB = Mean - 1.96 * se) 
  plot_title <- str_to_title(plot_title)
  p <- ggplot(data = plot_data, mapping = aes(x = Parameter, y = Mean)) +
    geom_point(size = 1) +
    geom_line() +
    geom_errorbar(aes(ymin = CLB, ymax = CUB)) +
    theme_light() +
    ggtitle(plot_title) +
    xlab(paste(plot_title, "Parameter")) +
    ylab("Clustering Coefficient")
  
  return(p)
}


### Analyzing Genes

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
    select(c(ParameterValue, Gene0_avg, Gene1_avg, Gene2_avg, Gene3_avg, Gene4_avg)) %>%
    group_by(ParameterValue) %>% 
    summarise(Gene0 = mean(Gene0_avg),
              Gene1 = mean(Gene1_avg),
              Gene2 = mean(Gene2_avg),
              Gene3 = mean(Gene3_avg),
              Gene4 = mean(Gene4_avg)) %>% 
    ungroup() %>%
    pivot_longer(cols = c(Gene0, Gene1, Gene2, Gene3, Gene4), names_to = "Gene", values_to = "Weight") %>% 
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
