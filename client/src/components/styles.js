const drawerWidth = 350;
export default theme => ({
    searchPaper: {
        padding: '2px 4px',
        display: 'flex',
        alignItems: 'center',
        width: 550,
    },
    root:{
        margin:'20px 0',
    },
    listPencarian:{
        position:"absolute"
    },
    paperTokok:{
        display: "flex",
        justifyItems: "center",
        margin: "2px 5px",
        padding: "0px 15px",
        
    },
    textProductTitle:{
        overflow:"hidden",
        height:41.5,
        textOverflow:"ellipsis",
        display:"box",
        lineClamp:2,
        boxOrient:'vertical',
        fontSize:15
    },
    containerProduct:{
        padding:5
    },
    priceNowProduct:{
        color:'#f57224',
        fontSize:18
    },
    priceDiscountProduct:{
        color:"#9e9e9e",
        fontSize:12,

    },
    discountPercentProduct:{
        color: "#9e9e9e",
        fontSize: 12,
    },
    wrapLocationProduct:{
        display:'flex',
        justifyContent:'flex-end'
    },
    locationProduct:{
        color: "#4a4747",
        fontSize: 15,
    },
    imgProduct:{
        width:"100%",
        maxHeight:"214px"
    },
    title:{
        fontFamily:`'Heebo', sans-serif`,
        fontWeight:900,
        fontSize:25,
        lineHeight:0
    },
    titleProductRoot:{
        fontFamily: `'Heebo', sans-serif`,
        fontWeight: 900,
        fontSize: 20,
        lineHeight: 0
    },
    subTitle:{
        textAlign:'center'
    },
    input: {
        marginLeft: 8,
        flex: 1,
    },
    iconButton: {
        padding: 10,
    },
    divider: {
        width: 1,
        height: 28,
        margin: 4,
    },
});