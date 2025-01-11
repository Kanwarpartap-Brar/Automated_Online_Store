import OrientDB from 'orientjs';

//connect to database using orientjs async function
async function connectToDatabase() {
    const client = await OrientDB.OrientDBClient.connect({
        host: "localhost",
        port: 2424
    });

    const session = await client.session({
        name: "demodb",
        username: "root",
        password: "Buckedup1!"
    });

    return { client, session }; // Ensure both client and session are returned
}

//function to get random products from the StoreProducts class
async function Products(session) {
    try {
        const results = await session.query('SELECT FROM StoreProducts').all(); //select from StoreProducts class
        const purchased_product = results[Math.floor(Math.random() * results.length)];
        return purchased_product;
    } catch (error) {
        console.error('Products failed:', error);
    }
}

//create order function
async function CreateOrder(session, product) {
    try {
        const quantity = Math.floor(Math.random() * 1000) + 1; //random quantity of product between 1 and 1000
        const TotalPrice = product.price * quantity; //calculates total price of an order
        const order = await session.command(`
            INSERT INTO StoreOrderSummary SET customer = (SELECT @rid FROM StoreCustomers LIMIT 1),
            order_total = :order_total, products = :products`, {
            params: {
                order_total: TotalPrice,
                products: [product['@rid']] //product id
            }
        }).one(); //get id of an order
        console.log('Order ID:', order['@rid']);
    } catch (error) {
        console.error('Failed CreateOrder:', error);
    }
}

//main function
async function main() {
    const { client, session } = await connectToDatabase();
    try {
        const product = await Products(session); //get product
        if (product) {
            await CreateOrder(session, product); //order once product is checked out
        }
    } catch (error) {
        console.error('Main function error:', error);
    } finally {
        await session.close();
        await client.close();
    }
}

//10 second interval in between creating orders
setInterval(main, 10000);





