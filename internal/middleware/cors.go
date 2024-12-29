package middleware

import (
	"github.com/devproje/balance-application/config"
	"github.com/gin-gonic/gin"
)

func CORS(ctx *gin.Context) {
	ctx.Header("Access-Control-Allow-Origin", config.Get().CorsOrigin)
}
