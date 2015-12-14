library(raster)
library(rgdal)
library(rgeos)

setwd("/Users/dougsponsler/Documents/Research/DustSim")

### Function for rounding to nearest 5
round5 <- function(x, r = 5) {
  round(x / r) * r
}

fsr_2015_landscape <- brick("/Users/dougsponsler/Documents/Research/vis_by_distance_raster/FSR_complete_2km_2015.tif") # rasterized GIS layer for 2015 FSR landscape

# Number code for landscape raster:
# 0 = road, impervious, water
# 1 = corn bloom2
# 2 = corn bloom1
# 3 = corn bloom0, corn undetermined bloom level
# 4 = other crop/undet bloom2
# 5 = other crop/undet bloom1
# 6 = other crop/undet bloom0, undetermined bloom level
# 7 = forest/treeline
# 8 = herb patch/line, roadside
# 9 = residential

hive_origin <- c(292263.656365, 4426271.356893)

distance_from_hive <- distanceFromPoints(fsr_2015_landscape, hive_origin) # distance raster on FSR 2015 extents (each cell = distance from center)
pVis <- calc(distance_from_hive, fun = function(x){ # a priori visitation probability of each cell based on its distance and the p(visitation) ~ distance function we fit to our dance data
  1.204e-01 * exp(-1.404e-03 * x)
  })
pVis_x1000 <- round5(calc(pVis, fun = function(x){x * 1000})) # multiply al visitation probabilities by 1000 and round to nearest 5
  summary(pVis_x1000)

### Procedure for creating a random sample of patches biased according to visitation probability
# starting values
vec <- c()
n <- 0
# parameters
pVis_min <- min(values(pVis_x1000))
pVis_max <- max(values(pVis_x1000))
num_patches = 10
# for loop
for(i in 1:length(unique(values(pVis_x1000)))) {
  # set.seed(1038)
  x <- sample(Which(pVis_x1000 == pVis_max - n, cells = TRUE), pVis_max - n) # loop works through raster cells in order of decreasing p(visitation), sampling a number of cells from each p(visitation) level equal to its p(visitation) x 1000 rounded to nearest 5
  vec <- append(vec, x)
  n <- n + 5 # a counter to adjust the p(visitation) level and the number of samples
}
forage_foci <- sample(vec, num_patches) # randomly draw 10 cells from the p(visitation)-biased vector of samples drawn above
forage_foci_coords <- xyFromCell(pVis_x1000, forage_foci) # convert cell indices to coordinates

### Procedure for scattering foragers around foraging loci
patch_size = 20
forage_scatter <- extract(pVis_x1000, forage_foci_coords, cellnumbers = TRUE, buffer = patch_size)
  scatter1 <- sample(forage_scatter[[1]][,1], 1000, replace = TRUE)
    scatter1_coords <- xyFromCell(pVis_x1000, scatter1)
  scatter2 <- sample(forage_scatter[[2]][,1], 1000, replace = TRUE)
    scatter2_coords <- xyFromCell(pVis_x1000, scatter2)
  scatter3 <- sample(forage_scatter[[3]][,1], 1000, replace = TRUE)
    scatter3_coords <- xyFromCell(pVis_x1000, scatter3)
  scatter4 <- sample(forage_scatter[[4]][,1], 1000, replace = TRUE)
    scatter4_coords <- xyFromCell(pVis_x1000, scatter4)
  scatter5 <- sample(forage_scatter[[5]][,1], 1000, replace = TRUE)
    scatter5_coords <- xyFromCell(pVis_x1000, scatter5)
  scatter6 <- sample(forage_scatter[[6]][,1], 1000, replace = TRUE)
    scatter6_coords <- xyFromCell(pVis_x1000, scatter6)
  scatter7 <- sample(forage_scatter[[7]][,1], 1000, replace = TRUE)
    scatter7_coords <- xyFromCell(pVis_x1000, scatter7)
  scatter8 <- sample(forage_scatter[[8]][,1], 1000, replace = TRUE)
    scatter8_coords <- xyFromCell(pVis_x1000, scatter8)
  scatter9 <- sample(forage_scatter[[9]][,1], 1000, replace = TRUE)
    scatter9_coords <- xyFromCell(pVis_x1000, scatter9)
  scatter10 <- sample(forage_scatter[[10]][,1], 1000, replace = TRUE)
    scatter10_coords <- xyFromCell(pVis_x1000, scatter10)

  scatter_all_coords <- rbind(scatter1_coords,
                              scatter2_coords,
                              scatter3_coords,
                              scatter4_coords,
                              scatter5_coords,
                              scatter6_coords,
                              scatter7_coords,
                              scatter8_coords,
                              scatter9_coords,
                              scatter10_coords)

forage_foci_coords.sp <- SpatialPoints(forage_foci_coords, proj4string = CRS("+init=epsg:26917")) # convert forage foci coordinates to SpatialPoints object
  buff1 <- gBuffer(forage_foci_coords.sp[1], width = 20, quadsegs = 50) # buffer each forage point by 20 m
  buff2 <- gBuffer(forage_foci_coords.sp[2], width = 20, quadsegs = 50)
  buff3 <- gBuffer(forage_foci_coords.sp[3], width = 20, quadsegs = 50)
  buff4 <- gBuffer(forage_foci_coords.sp[4], width = 20, quadsegs = 50)
  buff5 <- gBuffer(forage_foci_coords.sp[5], width = 20, quadsegs = 50)
  buff6 <- gBuffer(forage_foci_coords.sp[6], width = 20, quadsegs = 50)
  buff7 <- gBuffer(forage_foci_coords.sp[7], width = 20, quadsegs = 50)
  buff8 <- gBuffer(forage_foci_coords.sp[8], width = 20, quadsegs = 50)
  buff9 <- gBuffer(forage_foci_coords.sp[9], width = 20, quadsegs = 50)
  buff10 <- gBuffer(forage_foci_coords.sp[10], width = 20, quadsegs = 50)

### Create line from each forage point to origin
for(i in 1:length(forage_foci_coords[,1])) {
  assign(paste("line", i, sep = ""), SpatialLines(list(Lines(Line(rbind(forage_foci_coords[i,], hive_origin)), ID = "a"))))
}

### Calculate exposure
dust <- read.csv("/Users/dougsponsler/Documents/Research/DustSim_R/dust_data_model_parameterization.csv", header = TRUE, sep = ",")
dust_sub <- subset(dust, distance == 0 & lubricant == "FarmerChoice")

# in-field foraging
in_field_exp <- mean(dust_sub$conc)
foraged_patches <- extract(fsr_2015_landscape, scatter_all_coords) # extract landcover classes from landscape raster for each point in the scatter
fieldExposureCalc <- function(x) { # function for calculating exposure conditioned on landcover class, i.e. exposure only happens in corn fields (regardless of bloom level under these settings)
  ifelse(x > 0 & x < 4, in_field_exp, 0)
}
field_exposure <- fieldExposureCalc(foraged_patches) # vector of exposure level of each of the 10,000 "foragers"

# aerial contact
air_exposure_rate <- 0.01
airExposureCalc <- function(x) { # function for calculating exposure conditioned on landcover class, i.e. exposure only happens in corn fields (regardless of bloom level under these settings)
  air_exposure_rate * (length(x[x > 0 & x < 4]))
}
flyover_patches1 <- unlist(extract(fsr_2015_landscape, line1))
air_exposure1 <- airExposureCalc(flyover_patches1)

# drift zone foraging

# total exposure
exposure <- cbind(field_exposure, air_exposure)

### Visualizations
plot(pVis_x1000) # plot p(visitation) raster
  points(forage_foci_coords[, 1], forage_foci_coords[, 2], cex = 0.5, col = "blue") # plot forage_foci_coords

plot(fsr_2015_landscape) # plot landscape raster
  points(forage_foci_coords[, 1], forage_foci_coords[, 2], cex = 0.5, col = "blue") # plot forage_foci_coords
  lines(line1)
  lines(line2)
  lines(line3)
  lines(line4)
  lines(line5)
  lines(line6)
  lines(line7)
  lines(line8)
  lines(line9)
  lines(line10)

fsr_2015_landscape_buff1 <- crop(fsr_2015_landscape, buff1) # crop landscape raster to scatter buffer
plot(fsr_2015_landscape_buff1)
  lines(buff1)
  points(scatter1_coords[, 1], scatter1_coords[, 2], cex = 1, pch = 0) # plot forage_foci_coords

hist(exposure)
