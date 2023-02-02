library(tidyverse)

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
  p <- .plotting_function(plot_data, plot_title)
  print(p)
  dev.off()
}

.plotting_function <- function(plot_data, plot_title) {
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
