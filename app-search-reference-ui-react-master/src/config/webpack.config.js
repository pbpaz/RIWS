const path = require('path');

module.exports = {
  entry: './src/index.js', // Archivo principal de entrada
  output: {
    path: path.resolve(__dirname, 'dist'), // Carpeta de salida
    filename: 'bundle.js', // Nombre del archivo de salida
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // Archivos a procesar
        exclude: /node_modules/, // Ignorar la carpeta node_modules
        use: {
          loader: 'babel-loader', // Usar Babel para transformar archivos
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'], // Extensiones que Webpack debe resolver
  },
  devServer: {
    static: path.resolve(__dirname, 'dist'), // Carpeta para servir los archivos
    port: 3000, // Puerto del servidor de desarrollo
    open: true, // Abre el navegador automáticamente
  },
  mode: 'development', // Modo de desarrollo
};
