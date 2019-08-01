import {
    SEARCH
} from '../actions/types';
// import IsEmpty from '../validation/is-empty';

const initialState = {
    product_lazada:[],
    product_lazada_length:0,
    total_all_product:[],
    loading: false,
    showing_limit:15,
    keywords:[],
    hasMore:false,
    list_article:[],
    summary:{
        "TYPE": {
            description: "Ini menentukan fungsi produk, misalnya : televisi, laptop, komputer dan baju. ",
            values: []
        },
        "BRAND": {
            description: "Brand adalah merek dagang atau nama khusus yang mengidentifikasi   produk. Merek membuat produk dapat dibedakan dari kekacauan produk di pasar. Ini dapat berupa merek perusahaan, merek endorsed, atau merek produk individu.",
            values: []
        },
        "NAME": {
            description: "Atribut nama. Nama tersebut diberikan untuk varian produk yang ada dirilis dalam periode dan / atau area tertentu.Atribut nama produk di data beranotasi kami dapat berupa nomor seri atau ekstensi penamaan merek.",
            values: []
        },
        "COLOR": {
            description: "Atribut yang menjelaskan tentang warna produk. Warna tidak hanya basic colors (merah,kuning,hijau) tetapi bisa berupa exhaustive color (navy, copper gold).",
            values: []
        },
        "MATERIAL": {
            description: "Atribut yang menjelaskan bahan atau bahan utama dari produk itu dibuat.",
            values: []
        },
        "THEME": {
            description: "Atribut yang menggambarkan grafik yang dicetak pada produk. Biasanya terdiri dari serangkaian teks, bentuk, dan warna. Ini bisa berupa logo, lukisan, foto, atau judul entitas populer (seperti film, tokoh masyarakat, tim olahraga). Misalnya, botol termos hello kitty.",
            values: []
        },
        "DIMENSION": {
            description: "Dapat berupa panjang lebar atau volumen dari produk",
            values: []
        },
        "GENDER": {
            description: "Atribut untuk menargetkan suatu produk berdasarkan jenis kelamin. Pada judul produk terkadang terdapat informasi jenis kelamin seperti : Polo shirt pria warna hitam.",
            values: []
        },
        "SIZE": {
            description: "Atribut yang menjelasakan tentang standar ukuran dari suatu produk. Dapat berupa numeric atau nominal data (small,medium,large).",
            values: []
        },
        "MASS": {
            description: "Ini adalah satuan berat dari suatu produk atau berat dari produk.",
            values: []
        },
        "AGE": {
            description: "Beberapa produk di desain spesifik untuk beberapa golongan usia. Pada judul informasi tentang ini dapat berupa numeric, interval atau nominal (dewasa, balita, remaja).",
            values: []
        },
        "SHAPE": {
            description: "Atribut ini menggambarkan bentuk fisik suatu produk. Misalnya, cetakan kue ikan koi.",
            values: []
        },
        "CAPACITY": {
            description: "Atribut yang menjelaskan tentang kapasistas pada elektronik seperti laptop dan komputer. Misalnya Lenovo Ideapad 500GB.",
            values: []
        },
        "RAM": {
            description: "Berupa atribut yang menjelaskan besarnya RAM atau tipe dari RAM.",
            values: []
        },
        "OS": {
            description: "Atribut yang menjelaskan sistem operasi dari suatu produk. ",
            values: []
        },
        "PROCESSOR": {
            description: "Berupa informasi mengenai processor yang digunakan disuatu produk elektronik. ",
            values: []
        },
        // "GRAPHIC": {
        //     description: "",
        //     values: []
        // },
        // "STORAGE": {
        //     description: "",
        //     values: []
        // },
        // "DISPLAY": {
        //     description: "",
        //     values: []
        // },
        // "MEMORY": {
        //     description: "",
        //     values: []
        // },
        // "CPU": {
        //     description: "",
        //     values: []
        // },
        // "CAMERA": {
        //     description: "",
        //     values: []
        // },
    }
};


function findElement(element,index,data){
    // element adalah loop iterasi dari array
    //data adalah argument --> aksesnya pakai -->  this
    return element.bio === this[0] && element.name.toUpperCase() === this[1].toUpperCase();
}

export default function (state = initialState, action) {
    switch (action.type) {
        case SEARCH.loading:
            return {
                ...state,
                loading: true,
                keywords:action.payload
            }
        case SEARCH.remove_loading:
            return{
                ...state,
                loading:false,
                keywords:[]
            }
        case SEARCH.APPEND_DETIK_ARTICLE:
            return{
                ...state,
                list_article: [action.payload, ...state.list_article]
            }
        case SEARCH.loadMore:
            if (state.total_all_product.length > state.product_lazada){
                return {
                    ...state,
                    showing_limit: showing_limit * 2,
                    hasMore:true,
                    product_lazada: total_all_product.slice(0, showing_limit * 2)
                }
            }else{
                return{
                    ...state,
                    hasMore:false
                }
            }
            
        case SEARCH.APPEND_LAZADA_PRODUCT:
            const slice = state.product_lazada;
            const total_all_product= [action.payload, ...slice];
            
            const list_entity=action.payload.named_tag[0].map(x=>x);
      
            const summary = state.summary;
            list_entity.forEach(k => {
            
                if(k[0] !== 'O'){
                    let entity = k[0].replace(/^([A-Z]-)/g, '')
                    if (summary[entity]){
                    //    const value_entity = summary[entity].values.findIndex(xx=>xx.bio == k[0] && xx.name == k[1].toUpperCase());
                        const value_entity_index = summary[entity].values.findIndex(findElement,[k[0],k[1]]);
                        if (value_entity_index === -1){
                            summary[entity].values.push({
                                bio:k[0],
                                name:k[1],
                                value:1
                            });
                            summary[entity].values.sort((a, b) => (a.value < b.value) ? 1 : ((b.value < a.value) ? -1 : 0))
                        }else{
                            summary[entity].values[value_entity_index].value = summary[entity].values[value_entity_index].value +1;
                            summary[entity].values.sort((a, b) => (a.value < b.value) ? 1 : ((b.value < a.value) ? -1 : 0))
                        }
                       
                        // if(value_entity){
                        //     summary[entity].values.push([k[0], k[1], 1]);
                        // }
                    }
                 
                }
           
            });
       
            const new_p = total_all_product.slice(0,state.showing_limit)
            // console.log(summary[response_entity].values) 

            return{
                ...state,
                product_lazada_length:state.product_lazada_length+1,
                product_lazada: new_p,
                // hasMore: total_all_product.length > state.showing_limit && total_all_product.length > new_p.length ? true :false, 
                summary: summary
            }
        default:
            return state;
    }
}