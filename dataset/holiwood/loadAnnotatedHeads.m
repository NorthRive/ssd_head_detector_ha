function lAnnots = loadAnnotatedHeads(annotfile, scalename, anglename, imagespath, verbose, scaling)
% lAnnots = loadAnnotatedHeads(annotfile, scalename, anglename, imagespath, verbose, scaling)
% Reads Marcin's annotation files
%
% Input:
%  - annotfile: full path to file with annotations
%  - XXXname: string. Can be empty.
%  - imagespath: directory where images are found
%  - verbose: if >1, then images are displayed
%  - scaling: scale factor. Def. 1 (no scale)
%
% Output:
%  - lAnnots: struct-array with annotations 
%
% MJMJ/2010


if nargin < 6,
   scaling = 1;
end

if nargin < 5,
   verbose = 0;
end

if isempty(imagespath)
   verbose = 1;
end

fid = fopen(annotfile, 'rt');
if fid < 1,
   error(' Cannot open annotations file!');
end %

nimages = 0;
nix = 0;

stop = false;

while ~stop
   
   line = fgetl(fid);
   if line(1) ~= '#'
      error(' Invalid annotation header ');
   else
      nimages = nimages+1;
   end
   
   % Read content of current annotation
    % file:
    filestring = fgetl(fid);
    imgpath = sscanf(filestring, 'file: %s');
    
    if verbose
       disp(imgpath);
    end
    
    % newline
    foo = fgetl(fid);
    if ~isempty(foo) % Something is wrong, skip this entry
       discardDataUntilSymbol(fid, '#');
       continue
    end
       
    
    contobjs = true;
    
    while contobjs,
       % object:
       objstring = fgetl(fid);
       object = sscanf(objstring, 'object: %d');
       % bbox:
       bbstring = fgetl(fid);
       if isempty(bbstring) % Something is wrong, skip this entry
          discardDataUntilSymbol(fid, '#');
          break
       end
       bb = cell2mat(textscan(bbstring(6:end), '%n', 'delimiter', ','));    
       % scale:
       scalestring = fgetl(fid);
       scale = sscanf(scalestring, 'scale: %s');
       
       % fixpoints:
       pointsstring = fgetl(fid);     
       
       if isempty(pointsstring) % Something is wrong, skip this entry
          discardDataUntilSymbol(fid, '#');
          break
       end
            
       points = cell2mat(textscan(pointsstring(11:end), '%n', 'delimiter', ',')); 
       % angle:
       anglestring = fgetl(fid);
       angle = sscanf(anglestring, 'angle: %s');
       
       % orientation:
       oristring = fgetl(fid);
       orient = sscanf(oristring, 'orientation: %s');
       % newline
       foo = fgetl(fid);

       % Next line can be either another annotation in same frame or new image
       nextc = fgets(fid, 1);
       if feof(fid)
          stop = 1;
          break
       else
          if nextc == '#'
             if verbose > 2,
                disp(' End of image annotation');
             end
             fseek(fid, -1, 'cof');
             contobjs = false;
          end
       end
       
       skipit = true;
       if isempty(scalename) || any(strcmpi(scalename, scale)), %~isempty(strmatch(scalename, scale, 'exact')),
          if isempty(anglename) || any(strcmpi(anglename, angle)), %~isempty(strmatch(anglename, angle, 'exact')),
             nix = nix +1;

             [folder, bname, ext] = fileparts(imgpath);
             fullimgname = fullfile(imagespath, [bname ext]);

             if scaling ~= 1,
                bb(3:4) = bb(3:4) * scaling;
                w = bb(3);
                h = bb(4);
                bb(1) = bb(1)+(w/scaling-w)/2;
                bb(2) = bb(2)+(h/scaling-h)/2;                
             end
             
             lAnnots(nix).im = fullimgname;
             lAnnots(nix).x1 = bb(1);
             lAnnots(nix).y1 = bb(2);
             lAnnots(nix).x2 = bb(1)+bb(3);
             lAnnots(nix).y2 = bb(2)+bb(4);
             lAnnots(nix).orient = orient;
             lAnnots(nix).flip = 0; % Needed by pffVOC4
             
             skipit = false;
          end
       end
       
       if ~skipit && verbose > 1,
          [folder, bname, ext] = fileparts(imgpath);
          img = imread(fullfile(imagespath, [bname ext]));
          clf;
          imshow(img)
          
          title(bname);
          
          hold on
          hr = rectangle('Position', [bb(1) bb(2) bb(3) bb(4) ]);
          set(hr, 'EdgeColor', [1 0 0]);
          
          %pause
          keyboard
       end
       
    end

end % while

fclose(fid);

fprintf(' Total selected images: %d \n', nix);
