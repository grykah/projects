#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that takes pdf
ui <- shinyUI(fluidPage(
  
  titlePanel("File Upload"),
  
  sidebarLayout(
    sidebarPanel(
      fileInput('file_input', 'upload file ( . pdf format only)', accept = c('.pdf'))
    ),
    
    mainPanel(
      uiOutput("pdfview")
    )
  )
))

server <- shinyServer(function(input, output) {
  
  observe({
    req(input$file_input)
    
    test_file <- readBin(con=input$file_input$datapath,what = 'raw',n=input$file_input$size)
    writeBin(test_file,'SupplyandDemandAvocados.pdf')

  })
  
  output$pdfview <- renderUI({
    tags$iframe(style="height:600px; width:100%", src="myreport.pdf")
  })
  
})

# Run the application 
shinyApp(ui = ui, server = server)

