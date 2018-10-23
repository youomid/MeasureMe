const Sequelize = require('sequelize')

module.exports = {
    // sequelizer configuration
    db: {
        database: "mm_api_nodejs",
        user: 'mm_api',
        password: 'test',
        options: {
            dialect: 'postgres',
            host: '127.0.0.1',
            operatorsAliases: false
        }
    }
}