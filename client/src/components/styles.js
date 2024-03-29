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
    rootExpand: {
        width: '100%',
    },
    listPanel: {
      width:"100%"
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
        color: theme.palette.text.secondary,
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
    object_class:{
        fontSize:"12px",
        fontWeight:"bold",
        padding:"5px"
    },
    rootTitleText:{
        display:"flex",
        listStyle:"none",
        "& li":{
            padding:4
        }
    },
    titleArticle:{
        display: "flex",
        listStyle: "none",
        alignItems:'center',
        "& li": {
            padding: 4
        }
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
    titleNormal:{
        color:"#49494a",
        fontSize:"18px",
        lineHeight:"1.33",
        textDecoration:"underline"
    },
    sectionProductTitle:{
        lineHeight:2,
        fontWeight:"bold"
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
    sectionArticle:{
        lineHeight:1.8,
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