package serverTCP;

//refference : http://www.java2s.com/Tutorials/Java/Java_Network/0010__Java_Network_TCP_Server.htm
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketTimeoutException;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;


public class MainServerTcp {

	//static String end = "127.0.0.1";
	static int port = 4446;
	static int bytesMaxSize = 4096;
	static String absolutePath = "A:/ARQUIVOS WILL/FACULDADE/2019-01/TEBD/exercicio xml/arquivos/";

	public static void main(String[] argv) throws Exception {

		ServerSocket serverSocket = new ServerSocket(port, 100,
				InetAddress.getByName("localhost"));
		System.out.println("Server started  at:  " + serverSocket);
		serverSocket.setSoTimeout(10000);

		while (true) {
			System.out.println("Waiting for a  connection...");
			try {
				final Socket activeSocket = serverSocket.accept();

				System.out.println("Received a  connection from  " + activeSocket);
				Runnable runnable = () -> handleClientRequestFile(activeSocket);
				new Thread(runnable).start(); // start a new thread

			}catch(SocketTimeoutException e) {
				System.out.println("timeout listenning connections");
				continue;
			}
		}

	}

	public static File getOrCreatFile(String fileName) throws IOException {
		File file = new File(absolutePath + fileName);  
		if (!file.exists()) {  
			file.createNewFile();
		}
		return file;
	}

	public static String tratarChamadaDosMetodos(File f) {
		return XMLManipulation.executeMethod(f);
	}

	public static void handleClientRequestFile(Socket socket) {
		long tid = Thread.currentThread().getId();
		try{
			InputStream socketIn = null;
			OutputStream fileStreamRcv = null;

			while(socket.isConnected()) {
				socketIn = socket.getInputStream();

				byte [] rcvBytes = new byte[bytesMaxSize];

				int countIn = socketIn.read(rcvBytes);
				
				File commandFile = getOrCreatFile("Thread"+ tid +"-commandFile.xml");
				fileStreamRcv = new FileOutputStream(commandFile);

				
				fileStreamRcv.write((new String(rcvBytes, 0, countIn)).getBytes());
				fileStreamRcv.close();

				//trata validação do xml e decide qual função chamar
				String retorno = tratarChamadaDosMetodos(commandFile);
				BufferedWriter socketWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
				socketWriter.write(retorno);
				socketWriter.flush();
			}  
			socket.close();
		}catch(IOException e) {
			System.out.println("falha na manipulação de arquivos");
			e.printStackTrace();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

	public static void handleClientRequestMessage(Socket socket) {
		try{

			BufferedReader socketReader = null;
			BufferedWriter socketWriter = null;
			socketReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			socketWriter= new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

			String inMsg = null;
			while ((inMsg = socketReader.readLine()) != null) {

				System.out.println("Received msg from  client: " + inMsg);

				if(inMsg.equals("ENDCONNECTION")) {
					socketWriter.write("out");
					socketWriter.flush();
					break;
				}

				String outMsg = "servidor recebeu sua mensagem : '" + inMsg + "'";
				socketWriter.write(outMsg);
				socketWriter.flush();

			}
			System.out.println("fechando conexão do cliente");
			socket.close();
		}catch(Exception e){
			e.printStackTrace();
		}
	}

}
