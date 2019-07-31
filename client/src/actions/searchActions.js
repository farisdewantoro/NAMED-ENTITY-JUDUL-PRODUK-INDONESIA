import axios from 'axios';
import { SEARCH} from './types';
import io from '../socket_io'
export const loadingSearch = (data)=>{
    return{
        type:SEARCH.loading,
        payload:data
    }
}

export const searchProduct = (keyword)=>disbatch=>{
    disbatch(loadingSearch())
    io.emit('search_lazada', {keyword:keyword})
    // io.on('ner_keyword',(data)=>{
    //     disbatch(loadingSearch(data))
    // })
}

export const loadMore =()=>disbatch=>{
    disbatch({
        type:SEARCH.loadMore
    })
}

export const responseFromServer = ()=>disbatch=>{
    io.on('response_search_lazada',(data)=>{
        disbatch({
            type:SEARCH.APPEND_LAZADA_PRODUCT,
            payload: JSON.parse(data)
        })
    })
    io.on('response_search_detik', (data) => {
        console.log(data)
        disbatch({
            type: SEARCH.APPEND_DETIK_ARTICLE,
            payload: data
        })
    })
}

export const stopSearch = ()=>disbatch=>{
    io.emit('stop_searching',{search:false})
    disbatch({
        type:SEARCH.remove_loading
    })
}