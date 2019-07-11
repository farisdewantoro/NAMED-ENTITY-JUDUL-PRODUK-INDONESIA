import React from 'react'
import PropTypes from 'prop-types'
import {
    Card,
    CardContent,
    Button
} from '@material-ui/core'
const List_Lazada = props => {
    const { classes, data, handlerStopCrawling } = props;
    const NoImg = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png'

    return (

          <Card>
              <CardContent>
                <div>
                    {data.loading && (
                        <Button onClick={handlerStopCrawling} variant="contained" color="primary" style={{ position: "absolute" }}>
                            STOP CRAWLING
                    </Button>
                    )}
    
                    <h1 className={classes.titleProductRoot} style={{ textAlign: 'center' }}>
                        HASIL PENCARIAN DARI LAZADA
                        </h1>
                    <h1 className={classes.titleProductRoot} style={{ textAlign: 'center',padding:'15px 0' }}>
                        Total produk : {data.product_lazada_length}
                        </h1>
                </div>
                <div className='table-responsive' style={{maxHeight:400}}>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>
                                    NO
                      </th>
                                <th>
                                    TITLE
                      </th>
                                <th>
                                    PRICE
                      </th>
                                <th>
                                    LOCATION
                      </th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.product_lazada.map((d, i) => {
                                return (
                                    <tr onClick={()=>window.open(d.link,'_blank')}>
                                        <td>
                                            {i + 1}
                                        </td>
                                        <td>
                                            {d.title}
                                        </td>
                                        <td>
                                            {d.price_now}
                                            <br />
                                            <del>
                                                {d.discount_price} &nbsp; {d.discount_percent}
                                            </del>

                                        </td>
                                        <td>
                                            {d.location}
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>

                    </table>

                </div>
              </CardContent>
          </Card>
       
    )
}

List_Lazada.propTypes = {

}

export default List_Lazada
