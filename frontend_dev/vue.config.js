module.exports = {
  configureWebpack: {
    devtool: "source-map",
    devServer: {
      port: 3000,
      https: true,
      proxy: {
        "/auth/": {
          target: "https://localhost:5000",
          ws: true,
          changeOrigin: true
        },
        "/events/": {
          target: "https://localhost:5000",
          ws: true,
          changeOrigin: true
        }
      }
    },
  },
  outputDir: "../frontend",
  publicPath: "/frontend",
  transpileDependencies: [
    'vuetify'
  ]
}
