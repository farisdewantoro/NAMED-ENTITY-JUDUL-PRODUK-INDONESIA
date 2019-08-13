import React, { Component, Fragment } from 'react';

import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { compose } from 'redux';
import styles from './components/styles';
import Lazada from './components/Lazada';
import List_Lazada from './components/List_Lazada_img'
import moment from 'moment';
import { searchProduct, responseFromServer, stopSearch, loadMore } from './actions/searchActions';
import classNames from 'classnames';
import {
    Grid,
    Chip,
    Typography,
    Avatar,
    Card,
    CardContent,
    CardActionArea,
    GridList,
    GridListTile,
    CardHeader,
    Paper,
    InputBase,
    Divider,
    IconButton,
    Checkbox,
    LinearProgress,
    Button
} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import Slider from "react-slick";
import io from './socket_io'
import ProsesNer from './components/proses_ner'
import Summary from './components/Summary'
import Article from './components/Article_detik'
function prettyName(text) {
    if (text.length > 80) {
        text = text.substring(0, 72);
        return text + '...'
    }
    return text;
}

class App extends Component {
    constructor() {
        super();
        this.state={
            keyword:'',
            product_lazada:[]
        }
    }
    componentDidMount(){
        this.props.responseFromServer()
    
    }
  
    loadFunc = ()=>{
        console.log('LOAD MORE')
        this.props.loadMore()
    }
    handlerChangeText = (e)=>{
        this.setState({
            keyword:e.target.value
        })
    }
    handlerSubmitSearch = (e)=>{
        e.preventDefault();
        this.props.searchProduct(this.state.keyword)
    }
    handlerStopCrawling = ()=>{
        this.props.stopSearch()
    }
    render() {
        
        const { classes, searchs } = this.props;
        const { keyword, product_lazada,hasMoreData} = this.state;
        var settings = {
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 4,
            slidesToScroll: 1
        };
        let data ={
            title:"Promo Notebook Baru Asus A407MA-BV001T - Intel® Celeron® N4000 - RAM 4GB - 1TB - Intel UHD Graphics 600 - 14.0' - W10 - Grey - Laptop Murah (Gratis Tas) - Bergansi",
            price_now:"Rp3.909.000",
            location:"Jawa barat",
            discount_price:"Rp195.000",
            discount_percent:"-31%",
            img_link:"https://id-live-01.slatic.net/original/ddec71a6c64fc3d46b4f22cfc5466008.jpg",
            link:"https://www.lazada.co.id/products/denim-original-hitam-i143570579-s157343054.html?search=1"
        }
        return (
            <div className={classes.root}>
                {/* <div className={classes.listPencarian}>
                    <Paper className={classes.paperTokok}>
                        <Checkbox checked={true} value="gilad" />
                        <p>LAZADA</p>
                    </Paper>
                    <Paper className={classes.paperTokok}>
                        <Checkbox checked={true} value="gilad" />
                        <p>BUKALAPAK</p>
                    </Paper>
                    <Paper className={classes.paperTokok}>
                        <Checkbox checked={true} value="gilad" />
                        <p>TOKOPEDIA</p>
                    </Paper>
                </div> */}
             
                <Grid container direction="column" alignContent="center" justify="center">
                    <Grid item md={12}>
                        <h1 className={classes.title} style={{textAlign:'center'}}>
                          NAMED ENTITY EXTRACTION PADA JUDUL PRODUK 

                        </h1>
                        <p className={classes.subTitle}>
                            Ektraksi attribute menggunakan Conditional Random Field
                        </p>
                    </Grid>
                    {!searchs.loading && (
                        <Grid item md={12}>
                            <form onSubmit={this.handlerSubmitSearch}>
                                <Paper className={classes.searchPaper}>
                                    <InputBase
                                        className={classes.input}
                                        placeholder="Ketik disini"
                                        value={keyword}
                                        onChange={this.handlerChangeText}
                                        inputProps={{ 'aria-label': 'Cari !' }}
                                    />
                                    <IconButton className={classes.iconButton} aria-label="Search" onClick={this.handlerSubmitSearch}>
                                        <SearchIcon fontSize='large' />
                                    </IconButton>


                                </Paper>
{/* 
                                <span>*Keyword: laptop, handphone, baju, mouse dll</span> */}
                            </form>
                        </Grid>
                    )}
                    {searchs.loading && (
                        <Grid item md={12}>
                            <LinearProgress variant="query" style={{padding:5,margin:'10px 0'}}/>
                            <Button variant="contained" color="primary" fullWidth onClick={this.handlerStopCrawling}>    
                                STOP CRAWLING
                            </Button>
                        </Grid>
                    )}
                  
                </Grid>
                {/* <div style={{padding:10}}>
                    
                    <ProsesNer data={searchs} classes={classes} />           
                </div> */}
               
                {searchs.product_lazada.length > 0 && (
                      <Fragment>
                        <div style={{ marginTop: "10px" }}>
                            {/* <Article data={searchs}
                        classes={classes} /> */}
                            <List_Lazada
                                data={searchs}
                                classes={classes}
                                hasMoreData={searchs.hasMoreData}
                                loadFunc={this.loadFunc}
                                handlerStopCrawling={this.handlerStopCrawling} />
                        </div>
                        <Summary classes={classes} data={searchs} />
                      </Fragment>  
                ) }
        
              
              
               
            </div>
        );
    }
}

App.propTypes = {
    classes: PropTypes.object.isRequired,
    searchs: PropTypes.object.isRequired,
    searchProduct: PropTypes.func.isRequired,
}
const mapStateToProps = (state) => ({
    searchs: state.searchs
})
export default compose(withStyles(styles), connect(mapStateToProps, { loadMore,searchProduct, responseFromServer, stopSearch }))(App);
