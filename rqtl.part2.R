library(qtl) #acceder a la libreria qtl
mapthis <- read.cross("csv", "C:\\Users\\leova\\Downloads", "PoxKaC7A.csv", crosstype = "riself", estimate.map= FALSE )
mapthis <- orderMarkers(mapthis, map.function = 'haldane', chr="7A")
pull.map(mapthis, as.table = TRUE, chr="7A")
compareorder(mapthis, chr="4A", c(1:121), error.prob=0.005)
mapthis <- switch.order(mapthis, chr="4A", c(1:121), error.prob=0.005)