import {
    SEARCH
} from '../actions/types';
// import IsEmpty from '../validation/is-empty';
const initialState = {
    product_lazada:[],
    product_lazada_length:0,
    loading: false
};

export default function (state = initialState, action) {
    switch (action.type) {
        case SEARCH.loading:
            return {
                ...state,
                loading: true
            }
        case SEARCH.remove_loading:
            return{
                ...state,
                loading:false
            }
        case SEARCH.APPEND_LAZADA_PRODUCT:
            let slice = state.product_lazada;
            let new_p= [action.payload, ...slice];
            return{
                ...state,
                product_lazada_length:state.product_lazada_length+1,
                product_lazada: new_p
            }
        default:
            return state;
    }
}