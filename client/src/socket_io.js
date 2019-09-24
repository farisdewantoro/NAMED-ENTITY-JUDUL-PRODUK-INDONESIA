import socket from 'socket.io-client'

const io = socket.connect('https://named-entity-produk.herokuapp.com:25155')


export default io