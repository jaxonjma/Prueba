package com.jaxon.prueba.config;

import java.util.Properties;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseBuilder;
import org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.Database;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * Configure EntityManager and TrasactionManager
 *
 */

@Configuration
@EnableTransactionManagement
@PropertySource("classpath:application.properties")
@ComponentScan(basePackages="com.jaxon.prueba")
@EnableJpaRepositories("com.jaxon.prueba.repository")
public class PersistenceConfig {

	/**
	 * Defines H2 or Oracle Mode
	 */
	public static final Boolean H2MODE = Boolean.TRUE;

    @Autowired
    private Environment environment;

	@Bean
	public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
		
		LocalContainerEntityManagerFactoryBean entityManager = new LocalContainerEntityManagerFactoryBean();
		
		entityManager.setDataSource(dataSource());
		entityManager.setPackagesToScan("com.jaxon.prueba.model");

		HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();

		if(H2MODE) {
			vendorAdapter.setDatabase(Database.H2);
			vendorAdapter.setGenerateDdl(true);
		} else {
			entityManager.setJpaProperties(additionalProperties());
		}

		entityManager.setJpaVendorAdapter(vendorAdapter);
		return entityManager;
	}
	
	@Bean
	public DataSource dataSource(){
			return H2MODE ? this.dataSourceH2() : this.dataSourceOracle();
	}
	
    private Properties additionalProperties() {

    	Properties properties = new Properties();
        properties.put("hibernate.dialect", environment.getRequiredProperty("hibernate.dialect"));
        properties.put("hibernate.show_sql", environment.getRequiredProperty("hibernate.show_sql"));
        properties.put("hibernate.format_sql", environment.getRequiredProperty("hibernate.format_sql"));
        
        return properties;        
    }

	@Bean
	public PlatformTransactionManager transactionManager() {

		JpaTransactionManager txManager = new JpaTransactionManager();
		txManager.setEntityManagerFactory(entityManagerFactory().getObject());
		return txManager;
	}
	
	/**
	 * DataSource H2 mode
	 * 
	 * @return
	 */
	public DataSource dataSourceH2() {
		EmbeddedDatabaseBuilder builder = new EmbeddedDatabaseBuilder();
		return builder.setType(EmbeddedDatabaseType.H2).build();
	}

	/**
	 * DataSource Oracle mode
	 * @return
	 */
	public DataSource dataSourceOracle() {

	  DriverManagerDataSource dataSource = new DriverManagerDataSource();
      dataSource.setDriverClassName(environment.getRequiredProperty("jdbc.driverClassName"));
      dataSource.setUrl(environment.getRequiredProperty("jdbc.url"));
      dataSource.setUsername(environment.getRequiredProperty("jdbc.username"));
      dataSource.setPassword(environment.getRequiredProperty("jdbc.password"));

      return dataSource;
		
	}

}
