#ui.R
library(shiny)

genre_list <- c("Action", "Adventure", "Animation", "Children", 
                "Comedy", "Crime","Documentary", "Drama", "Fantasy",
                "Film.Noir", "Horror", "Musical", "Mystery","Romance",
                "Sci.Fi", "Thriller", "War", "Western")

shinyUI(fluidPage(
  titlePanel("Movie Recommendation System"),
  fluidRow(
    
    column(4, h3("Select Movie Genres You Prefer (order matters):"),
           wellPanel(
      selectInput("input_genre", "Genre #1",
                  genre_list),
      selectInput("input_genre2", "Genre #2",
                  genre_list),

    )),
    
    column(4, h3("Select Movies You Like of these Genres:"),
           wellPanel(
      # This outputs the dynamic UI component
      uiOutput("ui"),
      uiOutput("ui2"),

    )),
    
    column(4,
           h3("You Might Like The Following Movies Too!"),
           tableOutput("table")
           
    )
  ),
  
  fluidRow(
    column(12,
           helpText("This app was created with data from", 
                    a("MovieLens", href="https://grouplens.org/datasets/movielens/", target="_blank")),
           helpText("To see the background development code for this app, check", a("here", href = "https://github.com/grykah/projects/tree/master/MoviePredictor", target="_blank"))
           
    )
  )
))