/**
 * This tests the java.net.URL APIs.
 * Methods that are implemented in the API and who's functionality is tested: 
 * getFile - Return the file name of URL, or an empty string if one does not exist
 * openConnection - Returns a URLConnection instance that represents a connection to the remote object referred to by the URL
 * Class MalformedURLException - to indicate that a malformed URL has occurred
 * 
 * 
 */

package testNG;

import static org.testng.Assert.assertEquals;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class MyUnit {
	public class MyUnitTest {
		
		//Provide a number of reachable URLs 
		@DataProvider (name = "reachableURLs")
		public String[] list1() {
			return new String[] {"https://www.oracle.com", "http://abc.com"};
		}
		
	    //Provide a number of unreachable URLs
	    @DataProvider (name = "unreachableURLs")
		public String[] list2() {
			return new String[] {"https://www.oracle.com/nofile.asdf", "http://abc.com/nofile.asdf"};
		}
	    
	    //Provide a number of invalid URLs
	    @DataProvider (name = "invalidURLs")
		public String[] list3() {
			return new String[] {"httq://www.google.com", "http//www.google.com", "http/www.google.com"};
		}
	   
	    @Test()
	    public void getFile_ValidInput_FileIsReturned() throws MalformedURLException {
	        
	    	URL url = new URL("http://www.test.com/myfile.txt");
	        String result = url.getFile();
	            	       
	        assertEquals(result, "/myfile.txt");
	    }
	    
	    @Test()
	    public void getFile_InvalidInput_EmptyStringReturned() throws MalformedURLException {
	        
	    	URL url = new URL("http://www.test.com");
	        String result = url.getFile();
	            	       
	        assertEquals(result, "");
	    }
	    
	    //Input for testConnection is provided by the dataprovider "reachableURLs"
	    //This method tests if a wedaddress is reachable (HTTP 200 OK)
	    @Test(dataProvider = "reachableURLs", description = "Test for reachable URLs")
	    public void connect_ReachableAddress_Http200Response(String webaddress) throws Exception{
	    	
	    	URL url = new URL(webaddress);
	    	
	    	try {
	    	        HttpURLConnection urlConn = (HttpURLConnection) url.openConnection();
	    	        urlConn.connect();

	    	        assertEquals(HttpURLConnection.HTTP_OK, urlConn.getResponseCode());
	    	    } catch (IOException e) {
	    	        System.err.println("Error accessing the site");
	    	        e.printStackTrace();
	    	        throw e;
	    	    }
	    }
	    
	    @Test(dataProvider = "unreachableURLs", description = "Test for unreachable URLs")
	    public void connect_UnreachableAddress_Http404Response(String webaddress) throws Exception{
	    	
	        // .... similar with connect_ReachableAddress_Http200Response but different input
	    		URL url = new URL(webaddress);
	    	
	    		try {
	    				HttpURLConnection urlConn = (HttpURLConnection) url.openConnection();
	    				urlConn.connect();

	    				assertEquals(HttpURLConnection.HTTP_NOT_FOUND, urlConn.getResponseCode());
	    	    		} catch (IOException e) {
	    	        System.err.println("Error accessing the site");
	    	        e.printStackTrace();
	    	        throw e;
	    	    }
	    }

	    @Test(dataProvider = "invalidURLs", expectedExceptions = MalformedURLException.class, description="Test for MalformedURLException due to invalid input for constructor")
	    public void urlConstructor_InvalidUrlInput_MalformedExceptionThrown(String webaddress) throws Exception {
	    
	    	    URL url = new URL(webaddress);
	    }
	}
}

