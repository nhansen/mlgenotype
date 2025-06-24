setwd("/Users/nhansen/AlphaThal/paper/priorversions/Figure1KmerBased")

read_acc_file <- function(filename) {
  acc_df <- read.table(filename, header=FALSE, sep="\t")
  #names(acc_df) <-c("NTrain", "CVAcc", "PredAcc")
  names(acc_df) <-c("NTrain", "PredAcc", "CVAcc")
  return(acc_df)
}

covg_vals <- c(10, 20, 30, 40)
iterations <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
#ntrain_vals <- c(60, 120, 180, 240, 300, 360)
ntrain_vals <- c(120, 180, 240, 300, 360)

covg_acc_files <- function(covg) {
  files <- sapply(iterations, function(x) { paste("train_", covg, "x_", x, "/accuracy.txt", sep="") })
  return(files)
}

all_covg_dfs <- function(covg) {
  alldata <- lapply(covg_acc_files(covg), read_acc_file)
  return(alldata)
}

ntrain_acc_vals <- function(ntrain, allcovdf) {
  accvals <- sapply(iterations, function(x) {df <- allcovdf[[x]]; accval <- df[df$NTrain==ntrain, "PredAcc"]})
  return(accvals)
}

mean_acc_val <- function(ntrain, allcovdf) {
  return(mean(ntrain_acc_vals(ntrain, allcovdf)))
}

sd_acc_val <- function(ntrain, allcovdf) {
  return(sd(ntrain_acc_vals(ntrain, allcovdf))/sqrt(length(iterations)))
}

df_means <- function(allcovdf) {
  return (sapply(ntrain_vals, function(x) {mean_acc_val(x, allcovdf)}))
}

df_sds <- function(allcovdf) {
  return (sapply(ntrain_vals, function(x) {sd_acc_val(x, allcovdf)}))
}

data_10x_df <- all_covg_dfs(10)
data_20x_df <- all_covg_dfs(20)
data_30x_df <- all_covg_dfs(30)
data_40x_df <- all_covg_dfs(40)

sd_arrow_length=0.02
x_offset=list(-12.0*rep(1, length(ntrain_vals)), -4.0*rep(1, length(ntrain_vals)), 4.0*rep(1, length(ntrain_vals)), 12.0*rep(1, length(ntrain_vals))*rep(1, length(ntrain_vals)))
plot(ntrain_vals+x_offset[[1]], df_means(data_10x_df), xaxt="n", xlab="Number of Training Samples", xlim=c(90, 390), ylab="Mean Prediction Accuracy", ylim=c(0.86, 1.0), col="blue", pch=15, cex=1.2)
axis(1, at=ntrain_vals, las=2)
arrows(x0=ntrain_vals+x_offset[[1]], y0=df_means(data_10x_df)-df_sds(data_10x_df), x1=ntrain_vals+x_offset[[1]], y1=df_means(data_10x_df)+df_sds(data_10x_df), length=sd_arrow_length, angle=90, code=3, col="blue", lwd=2)
points(ntrain_vals+x_offset[[2]], df_means(data_20x_df), col="red", pch=16, cex=1.2)
arrows(x0=ntrain_vals+x_offset[[2]], y0=df_means(data_20x_df)-df_sds(data_20x_df), x1=ntrain_vals+x_offset[[2]], y1=df_means(data_20x_df)+df_sds(data_20x_df), length=sd_arrow_length, angle=90, code=3, col="red", lwd=2)
points(ntrain_vals+x_offset[[3]], df_means(data_30x_df), col="brown", pch=17, cex=1.2)
arrows(x0=ntrain_vals+x_offset[[3]], y0=df_means(data_30x_df)-df_sds(data_30x_df), x1=ntrain_vals+x_offset[[3]], y1=df_means(data_30x_df)+df_sds(data_30x_df), length=sd_arrow_length, angle=90, code=3, col="brown", lwd=2)
points(ntrain_vals+x_offset[[4]], df_means(data_40x_df), col="black", pch=18, cex=1.4)
arrows(x0=ntrain_vals+x_offset[[4]], y0=df_means(data_40x_df)-df_sds(data_40x_df), x1=ntrain_vals+x_offset[[4]], y1=df_means(data_40x_df)+df_sds(data_40x_df), length=sd_arrow_length, angle=90, code=3, col="black", lwd=2)

abline(v=c(150,210,270,330))
legend(290, 0.91, c("10x", "20x", "30x", "40x"), col=c("blue", "red", "brown", "black"), pch=c(15, 16, 17, 18), cex=c(1.2, 1.2, 1.2, 1.2), title="Read Coverage")

