# PACKAGE INSTALLER FUNCTION ##

pkgLoad <- function( packages = "for_bots" ) {
  
  if( length( packages ) == 1L && packages == "for_bots" ) {
    packages <- c( "uuid", "quantmod", "caret", "dplyr", "tidyverse",
                   "corrplot", "httr", "anytime", "ggplot2", "TTR",
                   "data.table", "lubridate", "data.table", "jsonlite", "POST"
    )
  }
  
  packagecheck <- match( packages, utils::installed.packages()[,1] )
  
  packagestoinstall <- packages[ is.na( packagecheck ) ]
  
  if( length( packagestoinstall ) > 0L ) {
    utils::install.packages( packagestoinstall,
                             repos = "http://cran.csiro.au"
    )
  } else {
    print( "All requested packages already installed" )
  }
  
  for( package in packages ) {
    suppressPackageStartupMessages(
      library( package, character.only = TRUE, quietly = TRUE )
    )
  }
  
}

## API Keys - BINANCE AND BOTS ##

binance_api <- "binance_api"
binance_secret <- "binance_secret"
bot_name <- "bot_name"
bot_key <- "bot_key"

## GET DATA FROM BINANCE FUNCTION ##

binance_get_data <- function(symbol,interval,limit) {
  
  url <- "https://api.binance.com/api/v3/klines"
  
  query_symbol <- paste0("symbol=",symbol)
  query_interval <- paste0("interval=",interval)
  query_limit <- paste0("limit=",limit)
  
  query <- paste0(query_symbol,"&",query_interval)
  query <- paste0(query,"&",query_limit)
  
  query_final <- query
  
  response <- GET(url, 
                  add_headers("X-MBX-APIKEY"= binance_api),
                  query= query_final, 
                  verbose())
  
  value = content(response)
  
  my_df <- as.data.frame(123)
  
  colnames(my_df)[1] <- "unix"
  my_df$open <- NA
  my_df$high <- NA
  my_df$low <- NA
  my_df$close <- NA
  my_df$volume <- NA
  my_df$trade_count <- NA
  my_df[1:limit,] <- c(1,2,3,4,5,6,7)
  
  
  for(i in 1:limit){
    my_df$unix[i] <- as.numeric(substr(value[[i]][[1]],1,10))
    my_df$open[i] <- as.numeric(value[[i]][[2]])
    my_df$high[i] <- as.numeric(value[[i]][[3]])
    my_df$low[i] <- as.numeric(value[[i]][[4]])
    my_df$close[i] <- as.numeric(value[[i]][[5]])
    my_df$volume[i] <- as.numeric(value[[i]][[6]])
    my_df$trade_count[i] <- as.numeric(value[[i]][[9]])
  }
  
  my_df$date <- anytime(my_df$unix)
  
  my_df <- my_df %>%
    arrange(date)
  
  return(my_df)
}


## Data ##

DATA <- binance_get_data(symbol = "DOGEUSDT",interval = "2h",limit = 100)



## BOTS API ORDER REQUEST FUNCTIONS

BOTS_signal <- function(symbol,side,bot_name,bot_key,limitPrice){
  
  BOTS_symbol = substr(symbol,1,(nchar(symbol) - 4))
  
  url <- "https://signal.revenyou.io/paper/api/signal/v2/placeOrder"
  
  body_list = list(signalProvider = jsonlite::unbox(bot_name),
                   signalProviderKey = jsonlite::unbox(bot_key),
                   extId = jsonlite::unbox(UUIDgenerate()),
                   exchange = jsonlite::unbox("binance"),
                   baseAsset = jsonlite::unbox(BOTS_symbol),
                   quoteAsset = jsonlite::unbox("USDT"),
                   type = jsonlite::unbox("limit"),
                   side = jsonlite::unbox(side),
                   limitPrice = jsonlite::unbox(limitPrice),
                   qtyPct = jsonlite::unbox("100"),   
                   ttlType = jsonlite::unbox("secs"),
                   ttlSecs = jsonlite::unbox("55"),
                   responseType = jsonlite::unbox("FULL"))
  
  response <- httr::POST(url,
                   add_headers("accept"= "application/xml",
                               "Content-Type" = "application/json"),
                   body = jsonlite::toJSON(body_list),
                   verbose())
  
  value = content(response,as = "text",encoding = "UTF-8")
  
  value_df = jsonlite::fromJSON(value) %>% as.data.frame
  
  status = value_df$status[1]
  
  return(status)
}


send_signal_buy <- BOTS_signal(symbol = "ETHUSDT",side = "buy",bot_name = bot_name, bot_key = bot_key,limitPrice)
send_signal_sell <- BOTS_signal(symbol = "ETHUSDT",side = "sell",bot_name = bot_name, bot_key = bot_key,limitPrice)
