import React,{Fragment} from 'react'
import PropTypes from 'prop-types'
import {
    Grid,
    Typography,
    Card,
    CardActionArea
} from '@material-ui/core';
import Carousel from 'nuka-carousel';
import Grow from '@material-ui/core/Grow';
const Lazada = props => {
    const { classes, data, handlerStopCrawling} = props;
    const NoImg = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png'
    return (
        
        <Fragment>
  
                    <div>
                <div>
                    <h1 className={classes.titleProductRoot} style={{ textAlign: 'center' }}>
                        HASIL PENCARIAN DARI LAZADA
                        </h1>
                </div>
                <div>
                    <Carousel slidesToShow={6} height={400} cellSpacing={8} >
                        {data.map((d,i) => {
                        return (
                        
                         <Grow in={true} key={i}>
                            <Card>
                                <CardActionArea className={classes.containerProduct} onClick={handlerStopCrawling}>
                                        <img src={d.img_link ? d.img_link : 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png'} alt="gg" className={classes.imgProduct} />
                                    <Typography className={classes.textProductTitle}>
                                        {d.title}
                                    </Typography>
                                    <div>
                                        <Typography className={classes.priceNowProduct}>
                                            {d.price_now}
                                        </Typography>
                                        <div>
                                            <del className={classes.priceDiscountProduct}>
                                                {d.discount_price}
                                            </del>
                                            <span className={classes.discountPercentProduct}>
                                                {d.discount_percent}
                                            </span>
                                        </div>
                                        <div className={classes.wrapLocationProduct}>
                                            <Typography className={classes.locationProduct}>
                                                {d.location}
                                            </Typography>
                                        </div>

                                    </div>
                                </CardActionArea>
                            </Card>
                        </Grow>
                            )
                        })}
                    </Carousel>
                </div>
                    </div>
            
         
        </Fragment>
    )
}

Lazada.propTypes = {
    classes:PropTypes.object.isRequired,
    data:PropTypes.array.isRequired
}

export default Lazada
