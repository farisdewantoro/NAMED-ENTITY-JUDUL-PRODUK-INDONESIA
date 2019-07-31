module.exports = {
    entry: './client/src',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpe?g|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name(file) {
                                /*if (env === 'development') {
                                  return '[path][name].[ext]'
                              }*/
                                return '[name]_[hash].[ext]'
                            },
                            publicPath: function (url) {
                                return url.replace('../', '/img/')
                            },
                        },
                        
                    },
                ],
            },
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    output: {
        path: __dirname + './client/src/dist',
        publicPath: '/',
        filename: 'bundle.js'
    },
    devServer: {
        // Display only errors to reduce the amount of output.
        stats: "errors-only",
        overlay: true,
        contentBase: './client/src/dist',
        // Parse host and port from env to allow customization.
        //
        // If you use Docker, Vagrant or Cloud9, set
        // host: "0.0.0.0";
        //
        // 0.0.0.0 is available to all network devices
        // unlike default `localhost`.
        host: process.env.HOST, // Defaults to `localhost`
        port: process.env.PORT, // Defaults to 8080
        open: true, // Open the page in browser
    },
}