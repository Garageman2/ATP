
library(formattable)
library("htmltools")
library("webshot")    

export_formattable <- function(f, file, width = "100%", height = NULL, 
                               background = "white", delay = 0.2)
{
  w <- as.htmlwidget(f, width = width, height = height)
  path <- html_print(w, background = background, viewer = NULL)
  url <- paste0("file:///", gsub("\\\\", "/", normalizePath(path)))
  webshot(url,
          file = file,
          selector = ".formattable_widget",
          delay = delay)
}


df<-read.csv("../output.csv")
range(df[2:31],na.rm = TRUE)


normalize<-function(cellval){
  if (is.numeric(cellval)){
    return (round(cellval / max(df[2:31],na.rm=TRUE),digits=3))
  }
  else {
    return (cellval)
  }
}

colRange <- colorRamp(c("#0000ff","#ff0000"))



format <- formatter('span',style = x ~ style(color = rgb(colRange(ifelse(is.na(x),0,x)),maxColorValue = 255)))

#format <- formatter('span',style = x ~ style(font.weight = "bold"))

final <- as.data.frame(lapply(df,normalize))
final[is.na(final)] <- 0
final[final < 0] <-0

names <- list(colnames(final[2:31]))
names <- lapply(names,format)


export_formattable(formattable(final,names),"table.png")
            