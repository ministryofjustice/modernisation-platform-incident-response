var path = require('path')
var CopyPlugin = require('copy-webpack-plugin')
var MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  entry: {
    all: './main.js'
  },
  mode: 'production',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.scss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          {
            loader: 'css-loader?url=false'
          },
          {
            loader: 'sass-loader'
          }
        ]
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      }
    ]
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: 'node_modules/govuk-frontend/govuk/assets', to: path.resolve(__dirname, 'dist/assets') },
        { from: 'node_modules/@ministryofjustice/frontend/moj/assets', to: path.resolve(__dirname, 'dist/assets') },
      ]
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css'
    }),
  ]
}
