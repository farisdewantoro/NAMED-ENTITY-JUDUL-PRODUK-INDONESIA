import React from 'react'
import PropTypes from 'prop-types'
import {Card, CardContent, Button} from '@material-ui/core'
import InfiniteScroll from 'react-infinite-scroller';

function renderTitle(data, classes) {
    let keys = Object.keys(data)
    let element =  data.map(key=>{

        return (
            <li style={{display:'grid'}}>
                <span className={key[0]}>
                    {key[1]}
                </span>
                <span className={classes.object_class}>
                    {key[0]}
                </span>
            </li>
        )
    })
   return element
}

function scrollingFunc(e){
    console.log('ada')
    console.log(e)
}

const List_Lazada = props => {

    const { classes, data, handlerStopCrawling, hasMoreData, loadFunc} = props;
    const NoImg = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg' +
            '/480px-No_image_available.svg.png'

    return (

        <Card>
            <CardContent>
                <div>
                    <h1
                        className={classes.titleProductRoot}
                        style={{
                        textAlign: 'left',
                        padding: '15px 0'
                    }}>
                        Total produk : {data.product_lazada_length}
                    </h1>
                </div>
                <div
                    className='table-responsive'
                    style={{
                        height:300,
                        overflow:'auto'
                    }}
                    >
                    {/* <InfiniteScroll
                        pageStart={1}
                        loadMore={loadFunc}
                        hasMore={hasMoreData}
                        loader={<div className="loader" key={0}>Loading ...</div>}
                        getScrollParent={scrollingFunc}
                        useWindow={false}
                    > */}
                    <table className="table">
                        <tbody>
                       
                                
                            {data
                                .product_lazada
                                .map((d1, i) => {
                                    return (
                                        <tr >

                                            <td className={classes.rootTitleText} onClick={() => window.open(d1.link,'_blank')}>
                                                {d1 && d1.named_tag.map(d2=>{
                                                    return  renderTitle(d2, classes)
                                                })}


                                            </td>

                                        </tr>
                                    )

                                })}

                        
                        </tbody>
                   

                    </table>
                    {/* </InfiniteScroll> */}
                </div>
            </CardContent>
        </Card>

    )
}

List_Lazada.propTypes = {}

export default List_Lazada
