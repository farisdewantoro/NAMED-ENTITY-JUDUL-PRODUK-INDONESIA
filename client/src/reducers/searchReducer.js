import {
    SEARCH
} from '../actions/types';
// import IsEmpty from '../validation/is-empty';
const initialState = {
    product_lazada:[],
    loading: false
};

export default function (state = initialState, action) {
    switch (action.type) {
        case SEARCH.loading:
            return {
                ...state,
                loading: true
            }
        case SEARCH.APPEND_LAZADA_PRODUCT:
            let slice = state.product_lazada.slice(0,10);
            let new_p= [action.payload, ...slice];
            console.log(new_p)
            return{
                ...state,
                product_lazada: new_p
            }
        default:
            return state;
    }
}