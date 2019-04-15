package serverTCP;

import java.util.ArrayList;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.DocumentBuilder;

import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;

public class XMLManipulation {

    public static String executeMethod(File content) {
        try {

            //1) Validar o xml da requisicao
            InputStream request = new FileInputStream(content);
            InputStream requestCpy = new FileInputStream(content);
            
            boolean valid = validateXMLSchema(request);

            //2) Ler o xml recebido(xml - requisicao)
            if(valid){

                DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
           
                Document doc = dBuilder.parse(requestCpy);
                
                doc.getDocumentElement().normalize();

                NodeList nListMetodo = doc.getElementsByTagName("metodo");
                Element metodo = (Element) nListMetodo.item(0);
                String nomeMetodo = metodo.getElementsByTagName("nome").item(0).getTextContent();

                NodeList nList = doc.getElementsByTagName("parametros");

                if(nomeMetodo.equals("getHistorico")){
                    Node nNode = nList.item(0);
                            
                    if (nNode.getNodeType() == Node.ELEMENT_NODE) {

                        Element eElement = (Element) nNode;
                        
                        Node nNodeMat = eElement.getElementsByTagName("parametro").item(0);
                        Element mat = (Element) nNodeMat;

                        String matricula = mat.getElementsByTagName("valor").item(0).getTextContent();
                        
                        String xmlHEResponse = getHistorico(matricula);

                        //Enviar a String em forma de bytes pro cliente
                        return xmlHEResponse;
                    }
                }
            }else{
                return "XML não é válido. Abortar.";
            }
            
        } catch (Exception e) {
            e.printStackTrace();
            return "Erro durante a exccução do método. Abortar.";
        }
        
        //Código nunca alcançável(Eclipse reclama se tirar :( )
        return null;

    }

    public static String getMatriculaXML(String pathFile){
        File fXmlFile = new File(pathFile);
        DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder = null;
		try {
			dBuilder = dbFactory.newDocumentBuilder();
		} catch (ParserConfigurationException e) {
            return "Erro durante a execução do getMatriculaXML. Abortar";
		}
        Document doc = null;
		try {
			doc = dBuilder.parse(fXmlFile);
		} catch (SAXException | IOException e) {
            return "Erro durante o parser do XML em getMatriculaXML. Abortar";
		}

        doc.getDocumentElement().normalize();

        NodeList nList = doc.getElementsByTagName("matricula");
        Element mat = (Element) nList.item(0);
        String matricula = mat.getTextContent();

        return matricula;
    }

    public static String XMLWithContent(String matricula) throws SAXException, IOException, ParserConfigurationException {

        String dirName = "database/";
        String mat = null;

        File directory = new File(dirName);

        File[] fList = directory.listFiles();

        for (File file : fList){
            if (file.isFile()){
                            	
                mat = getMatriculaXML(dirName + file.getName());
                if(matricula.equals(mat))
                    return dirName + file.getName();
            }
        }

        return null;
    }

    public static String transformFileContentToString(String filePath) throws IOException 
    {
        StringBuilder contentBuilder = new StringBuilder();
        Stream<String> stream = Files.lines( Paths.get(filePath), StandardCharsets.UTF_8);
        stream.forEach(s -> contentBuilder.append(s).append("\n"));
        return contentBuilder.toString();
    }

    public static String getHistorico(String matricula){
        //1) Varrer todos os arquivos xml e pegar o xml com a mesma matricula do parametro
    	String xmlPath;
    	String xmlContent;
    	
    	try{
            xmlPath = XMLWithContent(matricula);
        }catch (Exception e){
            return "Erro durante a execução do getMatriculaXML. Abortar";
        }

        try {
		//2) Converter o conteudo do XML do historico para String.
        xmlContent = transformFileContentToString(xmlPath);

        }catch (IOException e){
            return "Historico Escolar nao encontrado. Abortar.";
        }

        //3) Retornar o conteudo para ser enviado.
        return xmlContent;
    }

    //Validação do XSD da requisicao
    public static boolean validateXMLSchema(InputStream xmlSource){

        try {
            SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
            Schema schema = factory.newSchema(new File("requisicao.xsd"));

            Validator validator = schema.newValidator();
            validator.validate(new StreamSource(xmlSource));

        } catch (IOException | SAXException e) {
            System.out.println("Exception: " + e.getMessage());
            return false;
        }
        return true;
    }

}
