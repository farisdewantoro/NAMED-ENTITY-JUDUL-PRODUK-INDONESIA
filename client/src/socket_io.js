import socket from 'socket.io-client'

const io = socket.connect('http://127.0.0.1:5000')


export default io